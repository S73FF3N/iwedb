Wind Farm
=========

In the success map a wind farm is a geographical assignment to a windpark. Over the assignment of turbines, the windpark get more depth of information. A wind farm has the following properties:

    *  **Name**: Name of the wind park; For excample: Beesenstedt
    *   2nd Name: alternative denomination of the wind park; For excample: Salzatal
    *   Postal Code: For excample: 06198
    *   City: Place/city/community of the location; For excample: Salztal
    *   **Country**: For excample: Deutschland/Germany
    *   Latitude: geographical degree of latitude; For excample: 51.5755952
    *   Lomgitude: geographical degree of longitude: For excample: 11.7175713
    *   **Offshore**: location of the wind park (on- ore offshore); For excample: onshore
    *   Description: additional information as free text; For excample: "The primary wind park form the jear 2001 got complemented in 2006. As Well two WEA from 2001 got repowered in the jear 2015."

Wind Farm List
--------------

The wind farm list shows all usable wind parks from the database.
Whith the following filter the selection can be limited:

    *   Name: This filter affects on Name, 2nd Name and City
    *   Country: multiple selection possible
    *   Offshore: unknown/yes/no
    *   Postal code

Wind Farm Detail
----------------

The detail view of a wind farm includes a map view. Either the geographical place with a marker is shown here, which is described over the properties latitude and longitude, or the different turbines of the
wind farm are displayed, if the koordinates are available.

Next to the geographical infotmation of the wind park all information date back to the turbines. Because of this the number of the linked turbines and their tecnology is displayed in the first row. After this
the individual turbines are displayed. These are sorted by their states: planned/under construction, in production or dismantled.

Analog to the detail view of an actor, linked projects and contracts are listed at the bottom part. These are not seperated into direct and indirect: As soon as a turbine of the wind park is connected to a
Project / Pool Project / Contract, they going to be presented in the detail view of the wind farm. As well if available linked surveys are listet.

With the button "Edit all turbines" its possible to edit all or various turbines from the wind farm. By default all turbines from the wind park are selected in the formula field "Turbines". The properties of
the selected turbines can be edited in the formula. If one formlua field got filled, the propertie of all selected turbines got overwritten. If the field stays empty, the propertie of the turbines stay the
same. The fields "State" and "Offshore" are two exceptions. They are formual fields with list selection, so they always contain a selection. Because of this they always get updated for the selected turbines, so
its importand to just edit turbines with the same properties in "State" and "Offshore". Basically the function "Edit all turbines" is provided to make the editation of big number of turbines easier.

Wind Farm Form
--------------

The particularity of the formula from a wind farm is the difference between creating a formula of a new wind farm and the editation of it. To reduse the affort of creating a new wind farm, this coordinates
are generated automatically over the information from postal code / city and country. Over this the topographical center got defined. Because of this the quality of the koordinates get etter with the
completeness of the information to postal code / city and coutry. If just the contry was given, the koordinates going to be calculated in the middle of the country.

In the edit formula the properties latitude and longitude are visible. They are caused of the calcualteion from the geographical center. If more exact information of the geogramphical position are availabe,
its nessasary to edit them here.

When a new wind farm has to get add, when just amend a current?
---------------------------------------------------------------

The convention is: If wind turbines geograpfical form a unit, what means that there is no much space and no communal borders between them, just one wind farm have to get added.

This is independet from the used tecnology of the turbines.

If mor wind turbines are located in one commune, but there is much space between them, its neccesary to crate a new wind farm for every turbine. For excample:
Musterstadt-Nord and Musterstadt-Süd or Musterstadt-Stadtteil A and Musterstadt-Stadtteil B.