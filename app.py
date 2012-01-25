from flask import Flask, render_template, request
from werkzeug.wsgi import DispatcherMiddleware
from forms import form, WeatherForm
import suds
import rpclib
from rpclib.application import Application
from rpclib.decorator import srpc
from rpclib.interface.wsdl import Wsdl11
from rpclib.protocol.soap import Soap11
from rpclib.service import ServiceBase
from rpclib.model.complex import Iterable
from rpclib.model.primitive import Integer
from rpclib.model.primitive import String
from rpclib.server.wsgi import WsgiApplication

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/weather', methods=['POST', 'GET'])
def weather():
    form = WeatherForm(request.form)
    if request.method == "POST":
        if form.validate():
            client = suds.client.Client("http://wsf.cdyne.com/WeatherWS/Weather.asmx?WSDL")
            try:
                forecast = client.service.GetCityForecastByZIP(form.data['zipcode'])
                
            except:
                forecast = None
            return render_template("weather.html", form=form, forecast=forecast)
    return render_template("weather.html", form=form)

class HelloWorldService(ServiceBase):
    @srpc(String, Integer, _returns=Iterable(String))
    def say_hello(name, times):
        '''say hello to name and repeat number of times

        @param name the name to say hello to
        @param the number of times to say hello
        @return the completed array
        '''

        for i in xrange(times):
            yield 'Hello, %s' % name

#placeholder for alternative SOAP server using different data
class COPrivateSchoolService(ServiceBase):
    
    @srpc(String, Integer, _returns=Iterable(String))
    def find_school(city):
        '''takes the Colorado city from which to return a list of private schools within that city
        
        @param city the city where the private school is located
        @return the completed array
        '''
        pass
    
    @srpc(String, Integer, _returns=Iterable(String))
    def add_school(city):
        '''takes the Colorado city from which to return a list of private schools within that city
        
        @param city the city where the private school is located
        @return the completed array
        '''
	pass

soap_application =  rpclib.application.Application([HelloWorldService], 'tns', interface=Wsdl11(), in_protocol=Soap11(), out_protocol=Soap11())
wsgi_application = WsgiApplication(soap_application)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soap':        wsgi_application,
})

if __name__ == "__main__":
      app.run(debug=True)
