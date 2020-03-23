Turbine Model
=============

The Category Turbine Model define the technology of windpower system. Different to the category Tubine, which discribe the actual system, Turbine Model define the techical properties like perfomance
and rotor diameter.

An object got define completely by following properties. Properties who are written **fat** are obligatory.

    *   **Name**: Name of the technology, For excample: "V90"
    *   **Manufacturer**: Manufacturer company fo the technology, for excample: "Vestas"
    *   Technology Class: Description of the technology; For excample: "MD"
    *   Output Power: Nominal performence of the technology, for excample: "2000kW"
    *   Rotor Diameter: The diameter of the rotor in m, for excample: 90m
    *   Amount of Blades: For excample: 3
    *   **Offshore**: Possibility for using the technology offshore; Options: yes/no
    *   **Regulation**: Aerodynamic regulation of the wind turbine; Options: stall/pitch
    *   **Drivetrain**: Concept of drivetrain; Options: gearless/gearbox
    *   **Wind Class**: Wind class after IEC norm; For excample: IEC lla, IECS
    *   Total weight: Total weight of the wind energy plant in t; For excample: 439t
    *   Tower weight: Weight of the tower in t; For excample: 335t
    *   Hub weight: Weight of the hub in t; For excample: 68t
    *   Rotor weight: Weight of the rotor in t; For excample: 36t
    *   Cut in wind speed: Minimal wind speed in m/s, on which the wind turbine produces energy; For excample: 3m/s
    *   Nominal wind speed: Wind speed, where the wind turbine reaches its nominal output; For excample: 13,5 m/s
    *   Cut out wind speed: Maximal wind speed in m/s, on which the wind turbine produces output; For excmaple: 25 m/s
    *   Min. rotor speed: Minimal rotation speed of the rotor in rotation per minute; For excample: 8,2 r/m
    *   Max. rotor speed: Maximal rotation speed of the rotor in rotation per minute; For excmaple: 17,3 r/m
    *   First Installation: Year of market entry of the technology; For excample: 2004
    *   Produced until: Year of market exit of the technology; For excample: 2009
    *   Sound level: sound level of the wind turbine in dB; For excample: 80 dB
    *   ProductWeb Page: Product homepage of the manufacturer; For excample: http://vestas.com/v90
    *   Serviced by DWT: Statement, if and in whitch form DWT take the service of the technology in general; Options: No/Basic/Full Service
    *   Maintenance Hours: Specification of the yearly average of downtime in hours for service activities
    *   Description: Additional information in text form; For excample: first wind turbine in the 2MW area from the manufacturer Vestas  

Turbine Model List
------------------

The Turbine Model List shows all usable Turbine Models. The filters at the top can be used to narrow the selection. Following filters can get selected and used with the search button:

    *   Manufacturer: It's possible to choose more then one manufacturer
    *   Name: Name of the technology (without manufacturer name)
    *   Regulation: stall/pitch
    *   Drivertrain: gearless/gearbox
    *   Output Power: filters (from-to); just one box can be selected, input in kW
    *   Rotor Diameter: filters (from-to); just one box can be selected, input in m
    *   First Installation: filters (from-to); just one box can be selected, Form: yyyy-mm-dd
    *   Offshore: yes/no
    *   Serviced by DWT: Form: No/Basic/Full Service

At the bottom on the right side of the filters, the number of results are shown, after the search button got pressed.

The list view now shows the results. It lists one foto (if available), the manufacturer and type, the number of turbines of this type which are deposited in the database. With a click on one technology,
some details are shown.

Over the button "Add Turbine Models" new technologies can be added to the database. The button opens the "Turbine Model Form". The Buttom "Custom Export" exports the actual Turbine Model list to excel.

Turbine Model Detail
--------------------

The detail view is structured into the hadding, which shows the manufacturer and the type, the main part with pictures and all usable information and the map view.
At the right of the hadding its possible edit the information with the "Edit"-Button. As well its possible to add images with the "Add Image"-Button.
In the main part, all links and pictures of the technolgy are shown and on the right all properties which are filled.

Above the map view the number of Technologies from this technology in the database are displayed. If the coordinates are available, they are also in the map view. Also the number of turbines, which have a
contract with the Deutschen Windtechnik, are displayed in the next row. With a click on the plus-symbol on the right, the row expands. Now all turbines under contract are listed. They are linked to each
detail view.

The map shows all real turbines, which are saved in the database. This is an example for the relational link of the data in the database.

In each detail view the history of editing of the object is shown at the bottom. This makes the edits of each user transperent. Normally the edit history is folded. With a click on the row it can get
folded out.

With the comment function ("Add commetn") its possible to add comments and attach files to the "Turbine Model".

Turbine Model Form
------------------

The formula is used to edit and invest properties of the turbine models.
New turbine models can be added in the head menu over "New Turbine Model" or in the Turbine Model List with the button "Add Model". After choosing one of this options the formula is reched, where all
properties can get added. Required fields are marked with fed and red headdings. As well at some points fill in assistance is available.

After all required fields are filled, the new database entry can be added with the Submit-Buttons at the left corner on the bottom. Now you reach the detail view of the Turbine model automatically. If
one formula field doesent got filled correctly, the formula get reloaded with an error infortmaion.
