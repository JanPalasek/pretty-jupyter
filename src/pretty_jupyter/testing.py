def _get_y_location(driver):
    scroll_position_script = """
            var pageY;
            if (typeof(window.pageYOffset) == 'number') {
                pageY = window.pageYOffset;
            } else {
                pageY = document.documentElement.scrollTop;
            }
            return pageY;
        """

    return driver.execute_script(scroll_position_script)


def is_visible(element, driver, epsilon_px=10):
    return abs(element.location["y"] - _get_y_location(driver)) < epsilon_px