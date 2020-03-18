Turbine
=======

A turbine in the success map is a real existing wind turbine. They are characterised with the following properties:

    *   **Turbine ID**: Marking of the Turbine after international convection; For excample: SEN300855
    *   **Wind Farm**: Wind farm, in witch the turbine is located; For excample: Buchonia
    *   **Model**: Tecnology of the Turbine (Turbine Model); For excample: Senvion 3.2M114
    *   **Offshore**: location of the Turbine (on-/offshore); Options: yes/no
    *   Hub Height: Hub height of the WEA in m; For excample: 100m
    *   **State**: State of the WEA refering to the building progress; Option:(planned / under construction / in production / dismantled
    *   Commisioning (Year): Year of commisioning; For excample: 2013
    *   Commisioning (Month): Month of commisioning; For excample: 3
    *   Commisioning (Day): Day of commisioning; For excample: 30
    *   Dismantling (Year): Year of dismantling; For excample: 2018
    *   Dismantling (Month): Month of dismantling; For excample: 11
    *   Dismantling (Day): Day of dismantling; For excample: 30
    *   Repowered: In case of diamntling: Got the WEA repowered?; Option: yes/no
    *   Subsequent Turbine: In case of repowering: Which turbine refounds the dismantled WEA?; For excample: SEN300579
    *   Latitude: Latitude coordinate; For excample: 51.45878
    *   Longitude: Longitude coordinate; For excample: 6:51999
    *   OSM ID: Openstreetmap ID (Marking of the node); For excample: 272116284
    *   Developer: Actor, who planned the WEA; Multiple selection possible; For excample: Denker & Wulff AG
    *   Asset Management: Actor, who manage the WEA as asset; Multiple selection possible; For excample: BGZ Fondsverwaltung GmbH
    *   Commercial Operator: Actor, who performs the commercial management; Multiple selection possible; For excample: wdp windmanager
    *   Technical Operator: Actor, who performs the technical management; Multiple selection possible; For excample: Deutsche Windtechnik X-Service GmbH
    *   Service: Actor, who performs the service; Multiple selection possible; For excample: Deutsche Windtechnik Service GmbH & Co. KG

Turbine List
------------

Beside the filter and the tabular view also charts are displayed, which shows the properties of the turbines.

The following filter options are availabe:

    *   Wind Farm: Multiple selection possible
    *   Manufacturer: Manufacturer of the WEA; Multiple selection possible
    *   Model: Technology of the WEA (Turbine Model); Multiple selection possible
    *   Turbine ID: Marking of the WEA
    *   Offshore: Option: yes/no
    *   State: Option: planned / under construction / in production / dismantled
    *   Commisioning Year: Year of commisioning; Range filter (from-to); Year
    *   Dismantling Year: Year of dismantling; FAnge filter (from-to);Year
    *   Owner: Owner of the WEA; Multiple selection possible
    *   Developer: Developer of the WEA; Multiple selection possible
    *   Asset Management: Asset Management of the WEA; Multiple selection possibel
    *   Technical Operator: Technical operator of the WEA; Multiple selection possible
    *   Commercial Operator: Commercial operator of the WEA; Multiple selection possible
    *   Service: Service company of the WEA; Multiple selection possible
    *   Country: Country, where the WEA is located; Multiple selection possible

Six diagrams are displayed, which change, same as the map view, depending on which filter is used. Beside the manufacturer and the technology also the state, the country and the offshore-state are presented
as pie charts. A sixth chart shows the number of turbines depending on their commisioning year. When the pointer points on one of the charts, the number of turbines going to be displayed.

Turbine Detail
--------------

The map view in the detail view shows the geographical position of the WEA. If no coordinates are available, the map view is not displayed.

The other properties are listed tabular. The year of Commisioning / Dismanting is presented on a timeline.

Analog to the wind farm, linked (Pool)projects, contracts and expert reports are listed.

A particularity is the formula "Dublicate Turbine" at the top side of the detail view. With the formula turbines can be dublicated, which makes the creation of big wind farms whith WEA with the same
technology easier.

Turbine Form
------------

When creating or editing turbines, conventions have to be obsered, which are explained with the following questions.

The turbine ID is an explict mark of a wind turbine. Its builded out of the manufacturer shorting and the serial number.

The following field are just displayed, if the state of the turbine was set on "dismantled": Dismantlich(Year), Dismantling(Month), Dismantlich(Day), Repowered, Subsequent Turbine

What are the shortings of the manufacturers for the "Turbine ID"?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    *   Repower: R, For excample: R70345
    *   Senvion: SEN, For excample: SEN300345
    *   Nordex: NX, For excample: NX70345
    *   Südwind: SW, For excample: SW70345
    *   Enercon: E, For excample: E80345
    *   Fuhrländer: FL, For excample: FL123
    *   FWT: FWT, For excample: FWT123
    *   Vestas: V, For excample: V12345
    *   NEG Micon: no shortcut, For excample: 12345
    *   Siemens: SWT, For excample: SWT1000-234-05
    *   Dewind: DE, For excample: DE12345
    *   ENO ENERGY: ENO, For excample: ENO12345
    *   Gamesa: G, For excample: G100183636
    *   GE Energy: GE, For excample: GE12345

What is the procedure, if the Turbine ID is not availabel?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a turbine ID is not available, the following shema have to be used to name the turbine: <Wind farm Name><WEA-Number>

Fro Excample: Windpark Musterstadt mit 3 WEA
            Erste WEA: "Musterstadt01"
            Zweite WEA: "Musterstadt02"
            Dritte WEA: "Musterstadt03"

Its neccasary to always pay attetntion to leave no space between the WEA-Name and the WEA-Number. Also bfore singe-digit numbers a 0 have to be added.

How geographical coordinates can be determinded with the help of Openstreetmap and what means "Openstreetmap ID"(OSM ID)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Openstreetmap (OSM) is an Open-Source_Project for the collection and presentation of cartographical data. It´s available over https://www.openstreetmap.org/.

Many of the excisting wind turbines are mapped in Openstreetmap. They appear on the map in form of a WEA-Symbol if the zoom is big enough. One click on that symbol opens a dialogue. Here the field
"Objektanfrage" have to be valued. After this some objects are listed at the left side of the window. Under "Ähnliche Eigenschaften" a knot appears under the objects, which displays the wind turbine.
One click on this knot opens all information to this WEA, as well the coordinates. Every knot in OSM has a own OSM ID. This ID can be found in the headding of the knot. Either the headding just contains
the OSM ID or the OSM ID stands in brackets behind the headding.

How turbines with the same properties can be dublicated?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the top line of the detail view of a turbine the formula "Duplicate Turbine" exist. This serves for the duplication of many turbines with the same properties.

In the formula field just the number of dublicatet tubines habe to be entered. If a wind farm contains 6 WEA from the same type, the number "5" have to be entered, to dublicate the first WEA 5 times. Now
all information from the first Turbine are contained into the 5 others without the geographical information and the tubine ID.

Condition fro the dplication of a turbine is the correct procurement of the Turbin ID. This always have to enf on two numbers. The area before this two numbers is the trunk of the Turbine ID. If a Turbine
got duplicated, this two numbers get extracted and with a interation constantly generate new Turbine ID´s.

If the number of turbines got entered in the formula, the correctness of the turbine ID is controlled with "Duplicate turbine". If no error was detected, an other button ("Go") appears, which is used to
finish the duplucation. If a turbine of the WEA dont end on two numbers, the error report "Turbine could not be duplicated due to invalid turbine name" adppears.

After finishing the duplication, the user get transmitted to the detail view of the wind farm. Here the generated turbines arise.

One WEA can be maximal duplicated 999 times. If a wind park owns more than 100 wind turbines, the duplicated WEA have to be set with a turbine ID with the following pattern: "Windpark001".
