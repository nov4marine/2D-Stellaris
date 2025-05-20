
game_state = {
    "current_state": "main_menu",  # can be main_menu, gameplay, new_game, options, 
    "new_game_initialized": False,  

    "view_mode": "galaxy",  # or "solar_system"
    "selected_star": None,  # The star selected in the galaxy view
    "current_solar_system": None,  # The solar system currently being viewed
    "gameplay_initialized": False,

    # global management classes used in game
    "player_manager": None,
    "nations": None
}