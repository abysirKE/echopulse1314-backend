from fastapi import APIRouter
from .story import router as story_router
from .story_summary import router as summary_router
from .routes import router as main_router


router = APIRouter()
router.include_router(story_router)
router.include_router(summary_router)
router.include_router(main_router)
