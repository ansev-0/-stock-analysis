from datetime import datetime
from PIL import Image
import os
import plotly.graph_objects as go
from src.database.database import DataBasePublishInstagram


class ImageInfraestructure(DataBasePublishInstagram):

    _valid_formats = ('.jpg', '.png', '.jpeg')
    
    def __init__(self, path_icons, path_local_images):
        self._path_icons = path_icons
        self._path_local_images = path_local_images
        super().__init__('instagram')
        self._collection = self._database['image_layout']
    
    def get_icon(self, name):
        for _f in self._valid_formats:  
            p = os.path.join(self._path_icons, f'{name}{_f}')
            if os.path.exists(p):
                return Image.open(p)
        raise ValueError
    
    def get_color_candlestick(self, **kwargs):
        return {'increasing_line_color': 'rgba(45,87,40,255)',
                'decreasing_line_color': 'rgba(255,0,0,255)'}
        
    def save_local_image(self, img, data):
        os.makedirs(self._path_local_images, exist_ok=True)
        path_company = os.path.join(self._path_local_images, data['name'])
        os.makedirs(path_company, exist_ok=True)
        date_str = data['date'].strftime("%Y-%m-%d")
        path_company_today = os.path.join(path_company, date_str)
        os.makedirs(path_company_today,exist_ok=True)
        path_image = os.path.join(path_company_today,
                                  datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png')
        img.write_image(path_image)
        return path_image
        
    @DataBasePublishInstagram.try_and_wakeup
    def get_layout(self, name):
        data = self._collection.find_one({'name': name}, 
                                          projection={'layout': 1, 'large_name': 1,
                                                      'name': 0, '_id': 0})
        return self.build_layout(data['layout'], data['large_name'])
    
    @staticmethod
    def build_layout(layout, real_name):
        layout['xaxis']['title'] = go.layout.xaxis.Title(**layout['xaxis']['title'])
        layout['yaxis']['title'] = go.layout.yaxis.Title(**layout['yaxis']['title'])
        layout['xaxis'] = go.layout.XAxis(**layout['xaxis'])
        layout['yaxis'] = go.layout.YAxis(**layout['yaxis'])
        layout['title']['text'] = real_name
        return layout
        
        
        