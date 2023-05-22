import requests
import forest.map_view


def image(self, state):
    request = requests.get(f'{self.root}/image', params={'valid_time': state.valid_time, 'initial_time': state.initial_time, 'pressure': state.pressure, 'variable': state.variable})
    data = request.json()
    return data.get('result', self.empty_image())
