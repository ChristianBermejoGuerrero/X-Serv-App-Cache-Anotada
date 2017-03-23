#Christian Bermejo Guerrero
# Ejercicio 9.7 Cache Anotada 
import webapp
import urllib.request

class cache(webapp.webApp):

    cache = {}

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""
        peticion = request.split()
        metodo = peticion[0]
        recurso = peticion[1][1:]
        return (metodo, recurso)

    def process(self, parsedRequest):
        """Process the relevant elements of the request.
        Returns the HTTP code for the reply, and an HTML page."""
        metodo,recurso = parsedRequest
        if metodo == "GET":
            if recurso.split('/')[0] == "reload":
                url = recurso.split('/')[1]
                print(url)
                url = "http://" + url
                # REDIRECCION A LA URL
                httpCode = "302"
                htmlBody = "<html><meta http-equiv= 'Refresh'" \
                            + "content='0;url=" + url + "'>"
            else:
                try:
                    if recurso in self.cache.keys():
                        httpCode = "200 OK"
                        htmlBody = self.cache[recurso];
                        print("ENNTRAMS CACHE")
                    else:
                        url = "http://" + recurso
                        f = urllib.request.urlopen(url)
                        body = f.read().decode('utf-8')
                        #body = body.encode('utf-8').strip()
                        self.cache[recurso] = body
                        antes = body.find("<body")
                        despues = body.find(">",antes)

                        enlaces = "<a href=" + url + "> Página original  |  </a>" \
                                     + "<a href=/reload/" + recurso + "> Refresh </a>"
                        body = body[:despues+1] + enlaces + body[despues+1:]
                        httpCode = "200 OK"
                        htmlBody = str(body)
                except urllib.error.URLError:
                    httpCode = "404 Not Found"
                    htmlBody = "No has introducido ninguna url"
                except UnicodeDecodeError:
                    httpCode = "404 Not Found"
                    htmlBody = "DECODE ERROR"
        else:
            httpCode = "405 Method Not Allowed" #A request method is not supported gor the requested resource
            hmtlBody = "Metodo no permitido"
        print("CACHE: " + str(self.cache.keys()))
        return (httpCode,htmlBody)

if __name__ == '__main__':
    try:
        testCacheApp = cache("localhost", 1234)
    except KeyboardInterrupt:
        print ("\nClosing binded socket")
