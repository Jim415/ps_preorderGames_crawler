# Configuration file for game tracking system
# These lists can be easily modified to add new games or regions

# List of games to track (can be partial names - will match all packages/versions)
TRACKED_GAMES = [
    "Delta Force",
    "WUCHANG: Fallen Feathers", 
    "Ghost of Yōtei",
    "NBA 2K26",
    "Borderlands 4",
    "EA SPORTS FC™ 26"
]

# List of regions to track
TRACKED_REGIONS = [
    "en-hk",
    "en-us", 
    "ja-jp",
    "zh-hans-cn",
    "ko-kr",
    "de-de",
    "fr-fr",
    "en-gb",
    "en-ca",
    "es-mx"
]

# Database table name
TRACKING_TABLE_NAME = "PS_games"

def get_tracked_games():
    """Get the list of tracked games"""
    return TRACKED_GAMES.copy()

def get_tracked_regions():
    """Get the list of tracked regions"""
    return TRACKED_REGIONS.copy()

def add_tracked_game(game_name):
    """Add a new game to the tracking list"""
    if game_name not in TRACKED_GAMES:
        TRACKED_GAMES.append(game_name)
        return True
    return False

def add_tracked_region(region_code):
    """Add a new region to the tracking list"""
    if region_code not in TRACKED_REGIONS:
        TRACKED_REGIONS.append(region_code)
        return True
    return False

def remove_tracked_game(game_name):
    """Remove a game from the tracking list"""
    if game_name in TRACKED_GAMES:
        TRACKED_GAMES.remove(game_name)
        return True
    return False

def remove_tracked_region(region_code):
    """Remove a region from the tracking list"""
    if region_code in TRACKED_REGIONS:
        TRACKED_REGIONS.remove(region_code)
        return True
    return False 