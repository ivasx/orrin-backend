from library.views.LikedTracksView import LikedTracksView

# /api/v1/favorites/ is a frontend-facing alias for /api/v1/library/liked/
FavoritesView = LikedTracksView
