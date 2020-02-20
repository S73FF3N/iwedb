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
^^^^^^^^^^^^

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

The button "Custom Export"

