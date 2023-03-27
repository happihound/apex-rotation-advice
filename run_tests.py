import tests.test_main
import tests.test_gameMapImage
import tests.test_userMapImage
import tests.test_poi_coordinator

# Run the tests
# Test the main function
tests.test_main.test_main_association_all()
tests.test_main.test_main_association_create()
tests.test_main.test_main_association_view()
tests.test_main.test_main_findSafePath()
tests.test_main.test_main_noAssociationMode()
tests.test_main.test_main_noMapName()
tests.test_main.test_main_noProgramMode()
tests.test_main.test_main_noRatio_findSafePath()
tests.test_main.test_main_wrongMapName()
tests.test_main.test_main_wrongProgramMode()
tests.test_main.test_main_wrongRatio_findSafePath()
tests.test_main.test_main_validMaps()
print("All tests passed in test_main.py")

# Test the gameMapImage class
tests.test_gameMapImage.test_return_ratio_16by10()
tests.test_gameMapImage.test_return_ratio_4by3()
tests.test_gameMapImage.test_return_ratio_16by9()
tests.test_gameMapImage.test_return_image_16by10()
tests.test_gameMapImage.test_return_image_4by3()
tests.test_gameMapImage.test_return_image_16by9()
tests.test_gameMapImage.test_copy_16by10()
tests.test_gameMapImage.test_shape()
print("All tests passed in test_gameMapImage.py")

# Test the poi coordinator class
tests.test_poi_coordinator.test_convertCoordsToPoi()
tests.test_poi_coordinator.test_distanceBetweenPoi()
tests.test_poi_coordinator.test_findAllNearPoi()
tests.test_poi_coordinator.test_findPoiFromLocation()
tests.test_poi_coordinator.test_getNumberOfPoi()
tests.test_poi_coordinator.test_getPoi()
tests.test_poi_coordinator.test_getPoiList()
tests.test_poi_coordinator.test_getPoiListNames()
tests.test_poi_coordinator.test_getValidMapNames()
tests.test_poi_coordinator.test_loadMap_WE()
tests.test_poi_coordinator.test_makeCoordinator()
tests.test_poi_coordinator.test_poiListToNames()
print("All tests passed in test_poi_coordinator.py")

# Test the userMapImage class
tests.test_userMapImage.test_detectAspectRatio()
tests.test_userMapImage.test_findRedDots()
tests.test_userMapImage.test_getTargets()
tests.test_userMapImage.test_returnCropSize_4by3()
tests.test_userMapImage.test_returnCropSize_16by9()
tests.test_userMapImage.test_returnCropSize_16by10()
tests.test_userMapImage.test_returnValidAspectRatios()
tests.test_userMapImage.test_wrongApspectRatio()
print("All tests passed in test_userMapImage.py")

print("All tests passed")
