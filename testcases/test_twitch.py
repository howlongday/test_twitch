import time
from actions import MainActions

def test_twitch_search_and_scroll(browser, test_folder):
    main = MainActions(browser, test_folder)

    # Step 1 : go to Twitch
    print("\nStep 1 : go to Twitch")
    main.open_url('https://m.twitch.tv/')
    time.sleep(2)
    
    # Execute self-healing logic to clear unexpected popups
    print("     >>> Running self-healing logic for popups")
    main.auto_handle_popups()

    # Step 2 : click in the search icon
    print("Step 2 : click in the search icon")
    main.click_and_wait('a[href="/directory"]','input[data-a-target="tw-input"]')
    time.sleep(2)

    # Step 3 : input StarCraft II
    print("Step 3 : input StarCraft II")
    main.input_text('input[data-a-target="tw-input"]', 'StarCraft II')
    time.sleep(1)
    
    # Verify search suggestion for "StarCraft II" appears
    print("     >>> Verifying search suggestions")
    main.waitfor('a[href="/StarCraft II"]')
    
    # Navigate to Channels results page
    print("     >>> Navigating to Channel results")
    main.push_enter('input[data-a-target="tw-input"]','a[href*="type=channels"]')
    time.sleep(2)

    # Step 4 : scroll down 2 times
    print("Step 4 : scroll down 2 times")
    main.scroll(direction="down", times=2)
    
    # Step 5 : Select one streamer
    print("Step 5 : Select one streamer")
    main.click_and_wait('div.dAHeLj:nth-of-type(3) img[src*="thumb0"]','div[data-a-target="video-player"]')
    time.sleep(1)
    
    # Execute self-healing logic to clear unexpected popups
    print("     >>> Running self-healing logic for popups")
    main.auto_handle_popups()
    
    # Step 6 : on the streamer page wait until all is load and take a screenshot
    print("Step 6 : on the streamer page wait until all is load and take a screenshot")
    
    # Wait for the overlay loading mask to be removed from DOM/View
    print("     >>> Monitoring player loading status")
    main.wait_until_gone("div.player-overlay-background", timeout=5)
    
    # Ensure the video player has transitioned to 'playing' state
    print("     >>> Confirming video playback state")
    main.waitfor('button[data-a-player-state="playing"]')
    time.sleep(1)
    
    # Capture the final playback state for test verification
    print("     >>> Capturing final screenshot")
    main.take_screenshot("Final_Streamer_Page")
    print("Test Case Completed")