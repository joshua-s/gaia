# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.ui_tests_privileged.app import UiTestsPivileged
from gaiatest.apps.homescreen.regions.permission_dialog import PermissionDialog


class TestPrivilegedAppDevicePicturePrompt(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('UI tests - Privileged App', 'device-storage:pictures-read', 'prompt')

    def test_get_pictures_prompt(self):
        uiTestsPrivileged = UiTestsPivileged(self.marionette)
        uiTestsPrivileged.launch()

        deviceStorage = uiTestsPrivileged.tap_device_storage_option()
        deviceStorage.switch_to_frame()
        deviceStorage.tap_get_pictures_button_locator()

        permission = PermissionDialog(self.marionette)
        self.marionette.switch_to_default_content()
        permission.wait_for_permission_dialog_displayed()

        self.assertEqual(permission.permission_dialog_message,
                         u'UI tests - Privileged App would like to access your images.')

        permission.tap_to_confirm_permission()

        read_permission = self.apps.get_permission('UI tests - Privileged App', 'device-storage:pictures-read')
        self.assertEqual(read_permission, 'allow')

        write_permission = self.apps.get_permission('UI tests - Privileged App', 'device-storage:pictures-write')
        self.assertEqual(write_permission, 'allow')
