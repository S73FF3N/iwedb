Contract
========

Service contracts of the Deutsche Windtechnik are managed with help of the categorie "Contract". A contract is defined over the following properties:

    *   **Name**: Contract name; For excample: V-TB-105515-24-02-04
    *   File: Contract dokument as PDF
    *   **DWT Unit**: Unit of the Deutsche Windtechnik, who conclused the contract; For excample: DWTX
    *   **DWT Responsible**: Responsible Customer-/Contract-/Projectmanager of the Deutsche Windtechnik; Choice: User of the Success Map of the Group "Custom Relations"
    *   **Turbines**: Turbines, which are involved into the contract; For excample: SEN300488, SEN300489, SEN300490, SEN300491, SEN300492, SEN300493
    *   **Conract Partner**: For excample: Windpark Musterstadt GmbH & Co. KG
    *   **Start Date**: Contract start; For excample: 01.01.2019
    *   **End Date**: Contract ending; For excample: 31.12.2032
    *   Termination Date: Date of termination; For excample: 01.07.2019
    *   Termination Reason: Reason of termination; Options: Closure of WTG / Alternation of Contract / Breach of Agreement / Bankruptcy / Competition / Change of Ownership
    *   Average Remuneration: Average yearly remuneration per WEA in €; For excample: 35.000€
    *   Farm Availability: Availability guarantee (reffered to park) in percent; For excample: 97%
    *   WTG Availability: Availability guarantee (reffered to individual WEA) in percent; For excample: 96,5%
    *   Availability Type: Type of the availability guarantee; time based / energy based
    *   Remote Control: Service: Remote Control; Options: included / not included
    *   Maintenance: Service: Maintenance; Options: included / not included
    *   Additional Maintenance: Service: Additional Maintenance (for excample type IV); Options: included / not included
    *   Unscheduled Maintenance Personnel: Service: Personell for unscheduled maintenance; Options: included / not included
    *   Unscheduled Maintenance Material: Service: Material for unscheduled maintenance; Options: included / not included
    *   Main Components: Service: Exchange of main components (personell and material); Options: included / not included
    *   Exclusion: Components, which are not included in service; For excample: Rotor, transmission station
    *   Service Lift Maintenance: Service: Options: included / not included
    *   Inspection of Service Lift By certified body: Service: Options: included / not included
    *   Safety-related inspection (service lift, safety equipment, etc.): Service; Options: included / not included
    *   Repair service lift, safety equipment, etc.: Service; For excample: included / not included
    *   Exchange of service lift, safety equipment, etc.: Options: included / not included
    *   Rotor blade inspection: Service; Options: included / not included
    *   Videendoscopic inspection gearbox: Service; Options: included / not included
    *   Periodic inspection of WTG by independent experts: Service; Options: included / not included
    *   Electrical Inspection: Service; Options: included / not included
    *   External Damages: Service: Damages from the outside ("Force Majeure") as contract part; Options: included / not included
    *   Repair of pressure vessels: Service; Optioms: included / not included
    *   General Overhaul of working equipment: Service; Options: included / not included
    *   Condition Monitoring: Service: Monitoring of WEA-conditions with vibrancy sensors; Options: included / not included

Contract List
-------------

In the contract list all available contracts are listed tabular. Also these are illustrated in diagramms.

Custom Export
^^^^^^^^^^^^^

Analog to the projects, also contracts can be formated into Excel-Format over the button "Custom Export". Because of this they can get eddited again.

Filter
^^^^^^

With the following filters the selection of contracts can get limitated:

    *   DWT: Unit of the Deutsche Windtechnik, which concluded the contract; Multiple selection possible
    *   Contractual Pertner: Multiple selection posible
    *   Wind Farm: Multiple selection possible
    *   Manufacturer: Manufacturer of the WEA; Multiple selection possible
    *   Model: Technology of the WEA; Multiple selection possible
    *   Start Date: Start date of the contract; Range filter (from - to); Format: yyyy-mm-dd
    *   End Date: End date of the contract; Range filter (from-to); Format: yyyy-mm-dd
    *   DWT Responsible: Customer manager; Multiple selection possible

The contract type, which is displayed in the tabular overview, is based on the services, which are defined for the contract.

The diagramms illustrate the actual filter value. Beside the manufacturer, the technology and the contractual partner, also the country and its distribution get illustarted in a pie chart. The age of a
WEA got illustrated over a bar chart.

Terminated Contracts
--------------------

Beside the "Contract List" an analog contract list exist, which contains the terminated or expired contracts.

Terminated contracts have the special feature, that the reference "Terminated" shows up before contract start. Also the termination date and the termination reason is indicated in the detail view.

Contract Detail
---------------

The detail view of a contract, lists all properties of a contract. Under the contract name the scope of service is summarised. If it is a full maintenance (with/without large components), Basic (+) or remote
control, will be set in the selection of the individual scope of services. The contract dokument can be openned over the icon at the upper right side.

The individual scope of service are clustered in the four categories remote control, sheduled maintenance, suppression and main components. The green tick or the red "x" will show, if a scope of service is
integrated or not. So services with a green tick are included and those with a red "x" not. The same apply for optional services, which are listd at the bottom.

For each contract the possibility exist to crate individual comments and add dokuments to them. This possibility should also be used for demands, if there is no additional contract object.

Contracts can be terminated with the button "Terminate". After using the button a Formula appears, where the termination reason and date have to be enterred. Terminated contracts will be transferred from
"Contract List" into "Terminated Contract".

Contract Form
-------------

Beside the general properties like "Names", "DWT unit", "Contractual partner" and "Start-" or "Enddate" of the contract, the individual services and options are listed in the contract formula. A service is
included to a contract, if the accordingly box in the formula is filled. The formula field "Exclusions" defines the components, wich are included in the contract. Here a multiple selection is possible.

For the selection of the turbines, the help field "Winfarm" exist. If a windfarm is indicated, the selection of turbines in the field "Turbines" will be redused to the turbines of the selected winfarm. Also the
field "All turbines of selected wind farm?" will appear. If all turbines of the wind farm should be selected, the tick have to be set here. This saves the work from setting all ticks behind any turbine.
With setting the tick the field "Turbines" disappears.