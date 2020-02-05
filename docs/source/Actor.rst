Actor
=====

An actor is a company which is active in the wind industry. He have the following properties:

    *   **Name**: Name of the company; For excample: Deutsche Windtechnik X-Service GmbH
    *   Address: Postal address of the company; For excample: Heideweg 2-4
    *   Postal code: For excample: 49086
    *   City: For excample: Osnabrück
    *   **Country**: For excample Deutschland/Germany
    *   Phone: Phone Number; For excample: +49 541 38 05 38 100
    *   Mail: E-Mail address; For excample: info@deutsche-windtechnik.com
    *   Web: Homepage; For excample: http:\\deutsche-windtechnik.com
    *   Sector: sector of the company; Beispiel: Service, Technincal Operations
    *   Head Oranisation: holding company; For excample: Deutsche Windtechnik AG

Actor List
^^^^^^^^^^

The Actor List lists all usable companies of the database alphabetical. Over the button "Add Actor" new companies can be added. With "Custom Export" the actual list with the used filters get exported into
Excel. The following filters are available:

    *   Name: Name of the company 
    *   Country
    *   City
    *   Sector: Sector of the company; multiple selection possible

Actor Detail
^^^^^^^^^^^^

Under the name of the company and the Edit-Button properties of the actors are displayed.

Its possible to assign employees with the "Add Employee" button. They have the following properties:

    *   **Name**: First and last name of the employee; For Excample: Max Mustermann 
    *   Function: Function of the employee; For Excample: Head of Sales
    *   Phone: Phone Number; For Excample: +49 451 38 05 38 100
    *   Alternative Phone
    *   Mail: E-Mail address; For excample: info@deutsche-windtechnik.com
    *   Address: Postal address; For excample: Heideweig 2-4
    *   Postal Code: For excample: 49086
    *   City: For excample: Osnabrück

If a company got assigned to a holding company over the "Head Organisation", the row "Head Organisation occured, which lists all doughter companies of the head company. Also in the doughter company the 
head company get linked.

As soon as a turbine owns in the properties "Developer", "Asset Manager", "Technical Operator", "Commercial Operator", "Service" or "Owner" the same object as the actor, a row appears in the detail view. 
It says for how much WEA the actor "Developer" / "Asset Manager" / "Technical Operator" / "Service Provider" or "Owner" is. With one click on one row it folds out and shows all turbines, sorted by
technologies.

The employees are listed to their company in the detail view. For individual employees there also exist a detail view with all their properties. Also the formula for changing the 
employee properties can be opened with the "Shift"-Symbol. The formula is available over the detail view from the employee too ("Edit"). Over the button "Set inactive" employees also can get set inactive.
This should be used if an employee isn't a member of the company any more.

Below the employee Project/Pool projects and contents, in which the actor is involved, are listed. Here is a difference between "direkt" and "indirekt". There is a direct involvation, if the actor is
linked as a "Negotiation Partner" in he project.
