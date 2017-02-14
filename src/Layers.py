from ..Script import Script

from UM.Logger import Logger

class Layers(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Add meta-info GCodes",
            "key": "Layers",
            "metadata":{},
            "version": 2,
            "settings":{}
        }"""

    def execute(self, data):
        totalLayers = 0
        totalTime = 0

        previousLayerElapsed = 0
        havePrintGeneralMeta = False
        
        index = 0
        for layer in data:
            currentLayer = -1
            currentLayerElapsed = 0
            
            # Extract data from layer
            for line in layer.split("\n"):
                if totalLayers == 0 and line.startswith(";LAYER_COUNT:"):
                    totalLayers = int(line[13:])

                if totalTime == 0 and line.startswith(";TIME:"):
                    totalTime = float(line[6:])

                if line.startswith(";LAYER:"):
                    currentLayer = int(line[7:])
                                    
                if line.startswith(";TIME_ELAPSED:"):
                    currentLayerElapsed = float(line[14:])

            # Inject info into GCODE
            toInject = ""
            if havePrintGeneralMeta == False and totalLayers != 0 and totalTime != 0:
                layer = "M800 L%d S%d\n" % (totalLayers, 1000 * totalTime) + layer
                havePrintGeneralMeta = True
            
            if currentLayer != -1 and currentLayerElapsed != 0:
                layer = layer.replace(";LAYER:", "M801 L%d S%d\n;LAYER:" % (currentLayer, 1000 *(currentLayerElapsed - previousLayerElapsed)))
                previousLayerElapsed = currentLayerElapsed
            
            data[index] = layer
            index +=1 
      
        return data
