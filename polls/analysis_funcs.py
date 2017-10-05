from .models import WEC_Typ

class ChartData(object):
    def check_valve_data():
        data = {'name': [], 'output_power': []}

        valves = WEC_Typ.objects.all()

        for unit in valves:
            data['name'].append(unit.name)
            data['output_power'].append(unit.output_power)

        return data