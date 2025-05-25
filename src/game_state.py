
game_state = {
    "current_state": "main_menu",  # can be main_menu, gameplay, new_game, options, 
    "new_game_initialized": False,  
    "gameplay_initialized": False,

    "pygui_manager": None,  # pygame GUI manager

    # global management classes used in game
    "player_manager": None,
    "galaxy": None,
    "nations": None,

    "screen_width": 1920,
    "screen_height": 1080,
}