from geofeaturesapi.model import LOCIDatasetRenderer, GeoFeatureRenderer


# Mock class
class Request:
    def __init__(self, qsa_profile=None, qsa_mediatype=None):
        self.values = {
            '_profile': qsa_profile,
            '_mediatype': qsa_mediatype
        }


def setup():
    # make a Request
    r = Request(qsa_profile='dcat', qsa_mediatype='text/turtle')

    # use the Request to call LOCIDatasetRenderer
    actual = LOCIDatasetRenderer(
        r,
        url='https://linked.data.gov.au/dataset/qld-structural-framework'
    ).render()
    print(actual.response)


if __name__ == '__main__':
    setup()
