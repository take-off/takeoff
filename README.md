# takeoff
A test framework to verify device state before bringing into production. Users create modules that contain
a .test() method (signature documented in tests/README), then add the test name to the inventory. The testRunner
then runs all tests against the specified device.

Recommended as part of un-drain procedure - an automated undrain procedure should run this code first and cancel
the undrain if any tests fail.
