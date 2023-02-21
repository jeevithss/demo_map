import streamlit as sl
import folium
import pandas
import streamlit.components.v1 as components
import json

def create_map():
    data = pandas.read_csv("C:\Jeevith\Python\VS\E-globe\Volcanoes.txt")
    lat = list(data["LAT"])
    lon = list(data["LON"])
    elev = list(data["ELEV"])
    name= list(data["NAME"])


    def color_producer(elevation):
        if elevation<1000:
            return "green"
        elif 1000<=elevation<3000:
            return "orange"
        else:
            return "red"

    map = folium.Map(location = [35.2, -100], zoom_start = 6, tiles ="Stamen terrain")
    feature_group = folium.FeatureGroup(name="My map")

    for lt,ln,el in zip(lat, lon, elev):
        feature_group.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, popup = str(el)+' m', 
        fill_color = color_producer(el), color = "black", fill_opacity = 0.7, fill = True))

    map.add_child(feature_group)
    map.save("Map1.html")
    return map,lat,lon,name

def read_json():
    f=open("world.json")
    data=json.load(f)
    return data



def gui():
    sl.title("E-GLOBE")
    menu=['Homepage','Login',"Search","Logout"]
    select=sl.sidebar.selectbox("Menu",menu)
    if 'is_logged_in' not in sl.session_state:
        sl.session_state.is_logged_in=False
    if select =="Homepage":
        sl.subheader("Welcome to E-globe")
    elif select == "Login":
        cred={"Admin":"123","Jeevith":"249","Rsa":"214","Mitul":"305"}
        sl.subheader("LOGIN PAGE")
        if sl.session_state.is_logged_in==False:
            username=sl.sidebar.text_input("Username")
            password=sl.sidebar.text_input("Password",type='password')
            if sl.sidebar.button("Login"):
                if username in cred and cred[username]==password:
                    sl.success("Successfully logged in as {}".format(username))
                    sl.session_state.is_logged_in=True
                    sl.session_state.username=username
                else:
                    sl.warning("Invalid login credentials")
        else:
            sl.success("Already logged in as {}".format(sl.session_state.username))
    elif select=="Logout":
        if sl.session_state.is_logged_in==True:
            sl.success("{} logged out sucessfully".format(sl.session_state.username))
            sl.session_state.is_logged_in=False
            sl.session_state.username=None
    elif select=="Search":
        if sl.session_state.is_logged_in==True:
                m,lat,lon,name =create_map() 
                search=sl.selectbox("Search any volcano",name)
                order=name.index(search)
                new_map=folium.Map(location=[lat[order],lon[order]],zoom_start=10)
                components.html(new_map._repr_html_(),width=800,height=600)
        else:
            sl.warning("You have to login first")




gui()
        