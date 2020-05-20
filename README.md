# kicad_libraries

Nyx Aerospace internal KiCAD libraries.

## Footprint Rules
 - Use IPC recommendations wherever possible. This tool is helpful for generating IPC footprints: http://www.ipc.org/ContentPage.aspx?pageid=Land-Pattern-Calculator
 - Create an outline of the component on the F.Fab layer along with a textbox with the value %R so that we can generate pretty assembly drawings as a board output.

## Schematic Symbol Rules
For ease of BOM generation, schematic symbols should include the following fields:
 - Manufacturer
 - Manufacturer Part No
 - Supplier
 - Supplier Part No