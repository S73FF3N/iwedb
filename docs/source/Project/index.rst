Project
=======

Projects are sales activities, which are mostly based on one wind farm. A projects has the following properties:

    *   **Name**: Indication of the project; For excample: Hemme Weißes Moor
    *   **DWT**: Unit of the Deutsche Windtechnik, which is technological responsible; For excample: DWTX
    *   **Sales Manager**: Sales manager, who serve the project; For excample: Jörg Fuchs
    *   **State**: Progress of the project; Options: Potential / Coffee / Soft Offer / Hard Offer / Negotiation / Final Negotiation / Won / Lost / Canceled
    *   Probability: Probability, by which the contract will be concluded; For excample: 90%
    *   Offer Number: Clear number of the project; For excample: A20190034
    *   **Turbines**: WEA, which are involved in the project; For excample: SEN300488, SEN300489, SEN300490, SEN300491, SEN300492, SEN300493
    *   Wind Farm Information Sheet: Document, which summarise the information of the wind farm and it´s WEA. This document is attached to every contract from DWTX and DWTSARL.
    *   **Negotiation Partner**: Campany, the project was negotiated with; For excample: WindPlan Witthohn + Frauen GmbH & Co. KG
    *   Contact Person: Contact person of the negotiation partner; For excample: Matthias Frauen
    *   Customer Information Sheet: Document, which summarise the customer information. This document is atatched to every contract from DWTX and DWTSARL.
    *   **Contract**: Type of the potetial conclusion of contract; Options: New contract / Extension / Upgrade / Downgrade
    *   **Contract Type**: Scope of service of the potential contract; Options: Basic Maintenance / Full Maintenance without MC / Full MAintenance with MC / Remote Control / Spare Parts / Technical
                           Operations / Other
    *   Runtime: Runtime of the potential contract in jears; For excample: 5
    *   Price: Annual payment per WEA in €; For excample: 35000
    *   EBT: Margin reslutating out of the calculation in %; For excample: 15
    *   Request Date: Date of the first contact; For excample: 2019-01-17
    *   Start Operation: Date of potential conract start; For excample: 2020-08-02
    *   Contract Signature: Date of contract signature; For excample: 2018-11-12
    *   Awarding Reason: Reaso for taking / rejecting the project; Options: Price / Contract Design / Experience with DWT / Readiness / Regional Structures / Political Decision / Liability
    *   ZOP (machine & tower): Neccessity of a condition based check (machine & Tower) before contract start; Options: yes/no
    *   ZOP (rotor): Neccessity of a condition based check (rotor) before contract start; Options: yes/no
    *   Gearbox endoskopic inspection: Neccessity of a gearbox endoskopy before contract start; Options: yes/no

Project List
------------

The project list shows all projects, beginning with the last modified project. The filter state is basically set like just actually negotiated projects are listed. Won or lost projects are not displayed,
but its possible to show them over changing the filter options.

Over the use of the following filter, the selection of projects can be enclosed:

    *   Project Name: Name of the project
    *   DWT: Unity of the Deutsche Windtechnik; Multiple selection possible
    *   State: State of the project progress; Multiple selection possible
    *   Probability: Probability of conclusion of a contract in percent; Range filter (from - to)
    *   Scope: Scope of service of the potential contract; Multiple selection possible
    *   Manufacturer: Manfufacturer of the WEA; Multiople selection possible 
    *   Model: Technology (Turbine Model) of the WEA; Multiple selection possible
    *   Negotiation Partner: Multiple selection possible
    *   Contract signature: Period of the contract siganture; Range filter (from - to); Format: yyyy-mm-dd
    *   Commencement Date: Date of contract start; Range filter (from - to); Format: yyyy-mm-dd
    *   Requets Date: Period of the first contact; Range filter (form - to); Format: yyyy-mm-dd
    *   Contract: Type of conclusion of contract (Nex contract, Extension etc.); Multiple selection possible
    *   Offer Number
    *   Sales Manager: Responsible sales employee; Multiple selection possible
    *   Country: Multiple selection possible

If the "Customer Information Sheet" or "Windfarm Information Sheet" is not deposited 30 days before potention contract start (state "Negotiation"/"Final Negotiation"/"Won"), thr corresponding line will color 
read, to point the user to less information before contract start.

Analog to the "Turbine List" also for projects diagrams are available, which give a fast grafical overview over the distribution of the properties from the filtered projects. The followinf five properties 
are displayed as pie or bar charts: Project state, Scope of Service, Technology, Negotiation Partner and age of the WAE at contract start (bar chart).

Custom Export
^^^^^^^^^^^^^

The button "Custom Export" exports based on the actual filter value, the project list in Excel-Fomat. Through this a processing is possible.

Project Overview
^^^^^^^^^^^^^^^^

With the button "Project Overview" also the project list exports into Excel-Format. The filters are not applied here. This export is oriented on the format from "Projektübersicht DWT Group" in the drive 
"dwt international"

Project Detail
--------------

Beside the information listed directly in the formula, other project specific information are generated with funktions. They are listed in the detail view of the project. Among others the maximal age of
the turbine will be calculated. Also for every manufacturer from a wind enegy plant a technology manager get deposited in the system. This is a sales employee, who maintain all projects of one technology.
Also the operator of the turbine of the project is listed. Based on the annual charge per wind enegy plant, the annual and total compensation of the potential contract will be calculated.

If the project is a member of a primary pool project, this Information will be elucidated under the project name with "part of:" and a ling to the pool project.

To every project the files "Customer Information Sheet" and "Wind Famr Information Sheet" can be added now. These are annexes at the DWTX/SARL.

The button "Coordinates" allwos the export of coordinates from turbines linked to the project.

With the service bases which are deposited in the system, the to the project location closest service base, which is a member of the responsible unit and also matches technological, will be calculated over
a funktion. The linear distance will be given. Also a link to Google Maps is available, which shows the actual distance and the driving time between project location and service base.

The values for distance and driving time, which are provided by Google Maps, can now be used to provide the travelling expense at basic contracts over the formula "Driving Rate". The deposited formula
is based on 0,44 €/km travel costs and 37 €/h personnel costs. After using the "Calculate"-Button, the flat rates for weekdays, saturday, sundays and feast days will be calculated.

Another formula enables to show completed contracts in a radius from x kilometers around the project location. Therefor the wnated number of kilometers have to be entered in the formula and. After this the 
Calculate-Button must be pressed. After a short calculation time under the formula all contracts are listed, which are located in the valued radius.

Analog to this a formula exist, which shows all windparks in the database, whos´s WEA from a certain manufacturer in a certain radius around the project location show.

If reports are neccessary befor contract start, these are displayed tabular under "Expert Reports before operational commencement". Here every row shows one date per WEA.The coloured marking of a line
symbolized depending on the state and the planning date, if action is needed. Individual dates can be modified or deleted over the buttons "Ändern"/"Löschen".

To add Information from actual projects, a commentary function exist. With the button "Add Comment", the formula for creating a new comment is reachable. A comment is composed out of a text and optional a
attached file. Written comments are listed sloping by their creating or changing date. The crating date and the author of the comment are shown beside the text. The SHift-Symbol at the right can be used to 
edit the coment. If a new file was added, a Dokument-Symbol appears, which can be used to open the file. Commentaries from primary Pool Projects are adopted under the heading "Pool Project Comments"
automatic.

Project to Contract
^^^^^^^^^^^^^^^^^^^

If a project owns the state "Won", the button "Contract" appears at the upper right area from the detail view. It is used to transferring a project in a contract. The contract formula will open, which
assume the DWT unit, the turbines and the contracts start and final date from the project.

Create Initiation Document
^^^^^^^^^^^^^^^^^^^^^^^^^^

If a project owns the state "Won", the button "Initiation" appears at the upper right area from the detail view. With this button a PDF-Document will be created. It will make the maintenance of the project
information in other systems easiers. Already existing information from the project are used to fill specific fields in this formula. 

Project Form
------------

In the project formula the characteristic propertieas of a project are determined. The help texts under each field help to fill in the information correctly.

By giving the information of the DWT unti, it´s important to value the technological responsible unit, not inevitable the unot from the sales manager. The sales manager got determined initial. A changing
of the sales manager is just possible over the responsible unit or the adminitrators.

The state "Potential" says, that no customer contact happened until now. On "Coffee" already a non-binding contact took place. "Soft Offer" discribes a indicative, not binding offer, while "Hard Offer" a
binding offer shows. If you are in (final) negotiations, the state is "(final) Negotiation". Not successful projects are "Lost" or "Cancelled", won projects are "Won". The "Probability" depents on the
assesment from the sales manager.
