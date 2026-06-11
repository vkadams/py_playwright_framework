import pytest
import allure
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# This file provides:
# 1. Command-line options (browser, base URL, video, screenshots, etc.)
#    All custom options use the "--my-" prefix to avoid conflicts
#    with the pytest-playwright plugin's built-in options.
# 2. Hooks to track test results
# 3. Fixtures for browser setup and teardown
# 4. Screenshot, video, and trace attachments to Allure reports
# ========================================================================


# ----------------------------------------------------------------------------
# CREATE OUTPUT DIRECTORIES
# ----------------------------------------------------------------------------
for _dir in ["reports/videos", "reports/screenshots", "reports/traces", "reports/allure-results"]:
    Path(_dir).mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------------------------
# STEP 1: ADD COMMAND LINE OPTIONS (prefixed with --my- to avoid conflicts)
# ----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Adds command line options for test configuration.
    All options use the "--my-" prefix so they don't conflict with
    the pytest-playwright plugin's built-in options (--browser, --headed, etc.).

    Usage:
        pytest --my-browser=firefox --my-headed --my-video=on
    Or store defaults in pytest.ini under [pytest] > addopts.
    """
    parser.addoption("--my-browser", default="chromium", help="Browser: chromium, firefox, webkit")
    parser.addoption("--my-headed", action="store_true", help="Run in headed (visible) mode")
    parser.addoption("--my-base-url", default="https://tutorialsninja.com/demo/", help="Base URL for tests")
    parser.addoption("--my-video", default="retain-on-failure", help="Record video: on, off, retain-on-failure")
    parser.addoption("--my-screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    parser.addoption("--my-tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")


# ----------------------------------------------------------------------------
# STEP 2: HOOK TO TRACK TEST RESULTS (PASS/FAIL)
# ----------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures the test result (pass/fail/skip) after each test phase.
    This is used later in the page fixture teardown to decide
    whether to take screenshots, save traces, or attach videos.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


# ----------------------------------------------------------------------------
# STEP 3: FIXTURE 1 - BROWSER CONTEXT SETUP
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def browser_context(request):
    """
    Creates and manages the Playwright browser context.
    - Reads configuration from custom --my-* CLI options
    - Starts the Playwright browser
    - Enables video recording if configured
    - Cleans up automatically after each test

    NOTE: Hyphens in CLI option names are converted to underscores
          when using getoption(). e.g., --my-browser -> my_browser
    """
    # Read configuration values (hyphens become underscores in getoption)
    browser_name = request.config.getoption("my_browser")
    headed_flag = request.config.getoption("my_headed")
    video_option = request.config.getoption("my_video")

    print(f"[OK] Starting browser: {browser_name}")
    print(f"[OK] Headless mode: {not headed_flag} (headed={headed_flag})")

    # Start Playwright
    playwright = sync_playwright().start()

    # Launch the specified browser
    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(headless=not headed_flag)
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=not headed_flag)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=not headed_flag)
    else:
        raise ValueError(f"[FAIL] Unsupported browser: {browser_name}")

    # Create a browser context (optionally with video recording)
    if video_option in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()

    # Yield the context for use in tests
    yield context

    # Clean up after the test
    print("[CLEANUP] Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------------------------------
# STEP 4: FIXTURE 2 - PAGE CREATION AND TEST ARTIFACT MANAGEMENT
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(request, browser_context):
    """
    Creates a new browser page for each test.
    - Navigates to the base URL
    - Starts tracing (if enabled)
    - Captures screenshots, traces, and videos for failed tests
    - Attaches all artifacts to Allure report
    - Cleans up videos for passed tests (when retain-on-failure)

    IMPORTANT - Teardown order matters:
      1. Stop tracing (context must be open)
      2. Take screenshot (page must be open)
      3. Close page (finalizes video file)
      4. Attach/cleanup video (file is now complete)
    """
    # Read test configuration (hyphens become underscores)
    base_url = request.config.getoption("my_base_url")
    screenshot_option = request.config.getoption("my_screenshot")
    tracing_option = request.config.getoption("my_tracing")
    video_option = request.config.getoption("my_video")

    print(f"[INFO] Navigating to: {base_url}")

    # Start tracing if enabled
    if tracing_option in ["on", "retain-on-failure"]:
        print("[TRACE] Tracing enabled - capturing screenshots and actions")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    # Create and navigate to base URL
    page = browser_context.new_page()
    page.goto(base_url)

    # Yield the page to the test
    yield page

    # ------------------------------------------------------------------------
    # TEARDOWN: Manage artifacts (screenshots, videos, traces)
    # Order: tracing -> screenshot -> close page -> video
    # ------------------------------------------------------------------------
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    print(f"[RESULT] Test '{test_name}' result: {'[FAIL]' if test_failed else '[PASS]'}")

    # 1️⃣ STOP TRACING (must happen while context is still open)
    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        browser_context.tracing.stop(path=trace_path)
        print(f"[SAVE] Trace saved: {trace_path}")

        # Attach trace info to Allure report (ZIP not directly supported)
        if test_failed or tracing_option == "on":
            allure.attach(
                f"Trace file: {trace_path}\nView with: playwright show-trace {trace_path}",
                name=f"{test_name}_trace_info",
                attachment_type=allure.attachment_type.TEXT
            )
            print("[ATTACH] Trace info attached to Allure report")

    # 2️⃣ TAKE SCREENSHOT (page must still be open)
    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"[SAVE] Screenshot saved: {screenshot_path}")

        # Attach to Allure report
        allure.attach.file(
            screenshot_path,
            name=f"{test_name}_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        print("[ATTACH] Screenshot attached to Allure report")

    # 3️⃣ CLOSE PAGE (finalizes the video recording)
    page.close()
    print("[CLEANUP] Page closed (video file finalized)")

    # 4️⃣ ATTACH OR CLEANUP VIDEO (file is now complete after page.close())
    if video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None

        if video_path and Path(video_path).exists():
            if test_failed:
                # Attach video to Allure report on failure
                allure.attach.file(
                    video_path,
                    name=f"{test_name}_video",
                    attachment_type=allure.attachment_type.WEBM
                )
                print("[ATTACH] Video attached to Allure report")
            elif video_option == "retain-on-failure":
                # Delete video for passed tests (retain-on-failure mode)
                time.sleep(0.5)  # brief wait to ensure file is unlocked
                Path(video_path).unlink(missing_ok=True)
                print(f"[CLEANUP] Deleted video for passed test: {video_path}")
