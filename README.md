# MetaData Plugin

This plugin adds custom G-Code commands with printing progress informations. Data are gathered from Cura's comments.

 - `M800 Lnnn Snnn` Defines the total number `L` of layers and the total estimated duration `S` of the print
 - `M801 Lnnn Snnn` Defines the current Layer `L` and the estimated print duration `S` of this layer
