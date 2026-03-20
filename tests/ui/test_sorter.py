import pytest
from playwright.sync_api import Page, expect

from pages.ui.allo_tv_page import AlloTVPage


@pytest.mark.ui
def test_sorter(page: Page):
    allo_tv_page = AlloTVPage(page)
    allo_tv_page.navigate()
    allo_tv_page.close_promo_if_visible()

    expect(allo_tv_page.sort_toggle).to_be_visible()
    allo_tv_page.sort_by_name()
    expect(page.locator('.products-layout__item')).not_to_have_count(0)
