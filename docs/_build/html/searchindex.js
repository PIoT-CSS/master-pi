Search.setIndex({docnames:["MasterCSS","MasterCSS.controllers","MasterCSS.exceptions","MasterCSS.models","MasterCSS.mqtt","MasterCSS.tests","MasterCSS.validators","index","modules"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":2,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["MasterCSS.rst","MasterCSS.controllers.rst","MasterCSS.exceptions.rst","MasterCSS.models.rst","MasterCSS.mqtt.rst","MasterCSS.tests.rst","MasterCSS.validators.rst","index.rst","modules.rst"],objects:{"":{MasterCSS:[0,0,0,"-"]},"MasterCSS.cli":{load_user:[0,1,1,""],main:[0,1,1,""],start_flask:[0,1,1,""],start_mqtt:[0,1,1,""]},"MasterCSS.constant":{Constant:[0,2,1,""]},"MasterCSS.constant.Constant":{CAR_BODY_TYPES:[0,3,1,""],CAR_COLOURS:[0,3,1,""],CAR_COORDINATES:[0,3,1,""],CAR_FUEL_TYPES:[0,3,1,""],CAR_SEATS:[0,3,1,""]},"MasterCSS.controllers":{auth:[1,0,0,"-"],booking:[1,0,0,"-"],car:[1,0,0,"-"],templates:[1,0,0,"-"]},"MasterCSS.controllers.auth":{login:[1,1,1,""],logout:[1,1,1,""],register:[1,1,1,""],verify_login:[1,1,1,""]},"MasterCSS.controllers.booking":{book:[1,1,1,""],cancel:[1,1,1,""],confirm_booking:[1,1,1,""],view:[1,1,1,""]},"MasterCSS.controllers.car":{filter_car:[1,1,1,""],get_all_cars:[1,1,1,""],get_available_cars:[1,1,1,""],pickup_car:[1,1,1,""],return_car:[1,1,1,""],search_car:[1,1,1,""]},"MasterCSS.controllers.templates":{index:[1,1,1,""],login:[1,1,1,""],mybookings:[1,1,1,""],myinfo:[1,1,1,""],not_found:[1,1,1,""],oauth2callback:[1,1,1,""],register:[1,1,1,""],unauthorised:[1,1,1,""]},"MasterCSS.exceptions":{error_value_exception:[2,0,0,"-"]},"MasterCSS.exceptions.error_value_exception":{ErrorValueException:[2,4,1,""]},"MasterCSS.models":{booking:[3,0,0,"-"],car:[3,0,0,"-"],user:[3,0,0,"-"]},"MasterCSS.models.booking":{Booking:[3,2,1,""],BookingSchema:[3,2,1,""]},"MasterCSS.models.booking.Booking":{ACTIVE:[3,3,1,""],CANCELED:[3,3,1,""],CONFIRMED:[3,3,1,""],CalRef:[3,3,1,""],CarID:[3,3,1,""],Cost:[3,3,1,""],DateTimeBooked:[3,3,1,""],DateTimeEnd:[3,3,1,""],DateTimeStart:[3,3,1,""],Distance:[3,3,1,""],HomeCoordinates:[3,3,1,""],ID:[3,3,1,""],INACTIVE:[3,3,1,""],Status:[3,3,1,""],UserID:[3,3,1,""],getStatus:[3,5,1,""]},"MasterCSS.models.booking.BookingSchema":{Meta:[3,2,1,""],opts:[3,3,1,""]},"MasterCSS.models.booking.BookingSchema.Meta":{fields:[3,3,1,""]},"MasterCSS.models.car":{Car:[3,2,1,""],CarSchema:[3,2,1,""]},"MasterCSS.models.car.Car":{AgentID:[3,3,1,""],BodyType:[3,3,1,""],Bookings:[3,3,1,""],Colour:[3,3,1,""],Coordinates:[3,3,1,""],CostPerHour:[3,3,1,""],CurrentBookingID:[3,3,1,""],FuelType:[3,3,1,""],HomeCoordinates:[3,3,1,""],ID:[3,3,1,""],Image:[3,3,1,""],Make:[3,3,1,""],NumberPlate:[3,3,1,""],Seats:[3,3,1,""],TotalDistance:[3,3,1,""]},"MasterCSS.models.car.CarSchema":{Meta:[3,2,1,""],opts:[3,3,1,""]},"MasterCSS.models.car.CarSchema.Meta":{fields:[3,3,1,""]},"MasterCSS.models.user":{User:[3,2,1,""],UserSchema:[3,2,1,""]},"MasterCSS.models.user.User":{Email:[3,3,1,""],FirstName:[3,3,1,""],ID:[3,3,1,""],LastName:[3,3,1,""],Password:[3,3,1,""],PhoneNumber:[3,3,1,""],UserType:[3,3,1,""],Username:[3,3,1,""],get_id:[3,5,1,""]},"MasterCSS.models.user.UserSchema":{Meta:[3,2,1,""],opts:[3,3,1,""]},"MasterCSS.models.user.UserSchema.Meta":{fields:[3,3,1,""]},"MasterCSS.mqtt":{publish:[4,0,0,"-"],subscribe:[4,0,0,"-"]},"MasterCSS.mqtt.publish":{Publisher:[4,2,1,""]},"MasterCSS.mqtt.publish.Publisher":{convertImageToByteArray:[4,5,1,""],fr_publish:[4,5,1,""],on_connect:[4,5,1,""],on_disconnect:[4,5,1,""],on_publish:[4,5,1,""],publish:[4,5,1,""],send_end:[4,5,1,""],send_header:[4,5,1,""]},"MasterCSS.mqtt.subscribe":{Subscriber:[4,2,1,""]},"MasterCSS.mqtt.subscribe.Subscriber":{on_connect:[4,5,1,""],on_log:[4,5,1,""],on_message:[4,5,1,""],subscribe:[4,5,1,""]},"MasterCSS.tests":{test_auth:[5,0,0,"-"],test_booking:[5,0,0,"-"],test_car:[5,0,0,"-"],test_car_management:[5,0,0,"-"],test_fixture:[5,0,0,"-"]},"MasterCSS.tests.test_auth":{test_404_not_found:[5,1,1,""],test_dashboard_route:[5,1,1,""],test_login_invalid:[5,1,1,""],test_login_unregistered:[5,1,1,""],test_login_valid:[5,1,1,""],test_logout:[5,1,1,""],test_register_invalid:[5,1,1,""],test_register_valid:[5,1,1,""],test_render_index:[5,1,1,""],test_render_login:[5,1,1,""],test_render_register:[5,1,1,""],test_unauthorised:[5,1,1,""]},"MasterCSS.tests.test_booking":{test_booking_in_mybookings:[5,1,1,""],test_cancel_booking:[5,1,1,""],test_confirm_booking:[5,1,1,""],test_setup:[5,1,1,""],test_view_booking:[5,1,1,""]},"MasterCSS.tests.test_car":{test_filter_after_book:[5,1,1,""],test_filter_cars:[5,1,1,""],test_filter_invalid:[5,1,1,""],test_search:[5,1,1,""],test_search_location:[5,1,1,""],test_search_make:[5,1,1,""],test_search_not_found:[5,1,1,""],test_setup:[5,1,1,""]},"MasterCSS.tests.test_car_management":{test_add_car:[5,1,1,""],test_change_car_detail:[5,1,1,""],test_remove_car:[5,1,1,""],test_view_all_cars:[5,1,1,""],test_view_first_car:[5,1,1,""]},"MasterCSS.tests.test_fixture":{client:[5,1,1,""]},"MasterCSS.validators":{email_validator:[6,0,0,"-"],phone_validator:[6,0,0,"-"],username_validator:[6,0,0,"-"],validator:[6,0,0,"-"]},"MasterCSS.validators.email_validator":{EmailValidator:[6,2,1,""]},"MasterCSS.validators.email_validator.EmailValidator":{check:[6,5,1,""],message:[6,5,1,""]},"MasterCSS.validators.phone_validator":{PhoneValidator:[6,2,1,""]},"MasterCSS.validators.phone_validator.PhoneValidator":{check:[6,5,1,""],message:[6,5,1,""]},"MasterCSS.validators.username_validator":{UsernameValidator:[6,2,1,""]},"MasterCSS.validators.username_validator.UsernameValidator":{check:[6,5,1,""],message:[6,5,1,""]},"MasterCSS.validators.validator":{Validator:[6,2,1,""]},"MasterCSS.validators.validator.Validator":{check:[6,5,1,""],message:[6,5,1,""]},MasterCSS:{cli:[0,0,0,"-"],constant:[0,0,0,"-"],controllers:[1,0,0,"-"],database:[0,0,0,"-"],exceptions:[2,0,0,"-"],models:[3,0,0,"-"],mqtt:[4,0,0,"-"],tests:[5,0,0,"-"],validators:[6,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","exception","Python exception"],"5":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:attribute","4":"py:exception","5":"py:method"},terms:{"abstract":6,"boolean":[1,6],"byte":4,"class":[0,3,4,6],"default":1,"function":[1,4],"int":[0,3,4,6],"return":[0,1,3,4,6],"static":3,"true":3,Ute:0,__init__:[],abc:6,access:[1,5],activ:[1,3],add:[1,5],added:5,adding:5,address:4,after:5,against:6,agent:1,agentid:3,all:[1,5],ani:[1,4,6],api:3,app:[0,5],appear:5,arrai:4,auth:[0,5,8],authent:[1,5],author:1,authoris:1,avail:[1,5],base64decod:1,base:[0,1,2,3,4,5,6],been:1,being:4,between:1,bind:4,black:0,blue:0,bodytyp:3,book:[0,5,8],bookingschema:3,bool:6,broker:4,broker_port:[],buf:4,buffer:4,cafe:0,calendar:1,call:4,callback:[1,4],calref:3,cancel:[1,3,5],car:[0,4,5,8],car_body_typ:0,car_colour:0,car_coordin:0,car_fuel_typ:0,car_seat:0,carid:3,carlton:0,carschema:3,chang:5,check:[1,6],claredon:0,clear:1,cli:8,client:[4,5],colour:3,configur:[0,5],confirm:[1,3,5],confirm_book:1,connect:4,connel:0,constant:8,contain:[0,1,3,4,5],content:[7,8],context:0,control:[0,5,8],convert:4,convertimagetobytearrai:4,coordin:3,correct:[4,5],cost:[1,3],costperhour:[1,3],criteria:1,current:1,currentbookingid:3,cycl:0,dashboard:[1,5],data:[4,5],databas:[3,5,8],date:[1,5],datetim:[1,5],datetimebook:3,datetimedifferenceinhour:1,datetimeend:3,datetimestart:3,declar:3,definit:0,delet:1,descript:1,detail:[0,1,5],dict:[1,4],diesel:0,disconnect:4,distanc:3,doesn:5,elizabeth:0,els:1,email:[1,3],email_valid:[0,8],emailvalid:6,end:[1,4],entri:5,env:0,environ:0,err:1,error:[1,2,6],error_value_except:[0,8],errorvalueexcept:[1,2],event:1,except:[0,8],exist:[1,5],ext:3,facial:4,featur:5,field:[3,5],file:4,file_nam:4,filenam:4,filter:[1,5],filter_car:1,first:5,firstnam:3,fitzroi:0,flag:4,flagstaff:0,flask:[0,3,5],flask_login:3,flask_marshmallow:3,flinder:0,foreign:3,form:1,format:1,found:1,fr_publish:4,from:1,fueltyp:3,garden:0,get:[1,3,6],get_all_car:1,get_available_car:1,get_id:3,getstatu:3,given:[1,4],googl:1,green:0,handl:[1,4],has:[1,3],hash:1,hatchback:0,have:1,header:4,histori:1,home:1,homecoordin:3,homepag:1,host:0,hotsel:0,hous:0,html:[1,5],http:3,ident:[0,3],identifi:4,imag:[3,4],inact:[1,3],index:[1,5,7],inform:[0,1,5],initi:4,initialis:[0,4],instanc:[4,5],integ:4,invalid:[1,5],item:4,its:3,json:[1,4],kei:3,king:0,kwarg:3,lastnam:3,latest:3,level:4,list:1,listen:4,load:0,load_us:0,locat:5,lock:1,log:[1,4,5],loge:1,logic:[3,4],login:[1,3,5],logout:[1,5],main:0,make:[1,3,5],manag:5,mangement:5,marshmallow:3,mastercss:7,match:1,melbourn:0,member:4,messag:[1,2,4,5,6],meta:3,method:[],mixin:3,model:[0,8],modul:[7,8],more:5,mpv:0,mqtt:[0,8],mqtt_log_debug:4,mqtt_log_err:4,mqtt_log_info:4,mqtt_log_notic:4,mqtt_log_warn:4,mqttmessag:4,msg:4,mybook:[1,5],myinfo:1,name:4,none:[1,2,3],northsid:0,not_found:1,number:[0,1,3],numberpl:3,oauth2:1,oauth2callback:1,oauth2credneti:1,object:[0,3,4],on_connect:4,on_disconnect:4,on_log:4,on_messag:4,on_publish:4,one:5,opt:3,option:1,orang:0,otherwis:1,out:1,overlap:1,packag:[7,8],page:[1,5,7],paramet:[0,1,3,4,5,6],password:[1,3,5],pattern:6,payload:[1,2,4],petrol:0,phone:1,phone_valid:[0,8],phonenumb:3,phonevalid:6,pick:1,pickup:1,pickup_car:1,pickup_datetim:1,point:1,popul:5,port:0,previou:5,privat:4,project:0,prompt:1,publish:[0,8],purpl:0,pytest:5,qos:4,qualiti:4,queen:0,queensberri:0,rais:1,rang:1,rathdown:0,readthedoc:3,receiv:4,recognit:4,red:0,redirect:1,referer:3,regex:6,regist:[1,5],relat:5,remov:5,render:[1,5],render_pag:1,render_templ:1,repres:3,request:1,requir:1,respons:4,rest:2,result:[1,4,6],retain:4,return_car:1,return_datetim:1,rout:[1,4,5],rtype:[1,4],run:4,salt:1,schema:3,schemaopt:3,search:[1,5,7],search_car:1,seat:3,secur:5,sedan:0,seen:5,self:[],send:4,send_end:4,send_head:4,sent:4,serversid:2,servic:4,session:1,set:4,setup:[0,5],sever:4,share:0,should:5,show:5,specifi:4,sport:0,sqlalchemi:3,start:0,start_flask:0,start_mqtt:0,statu:[1,3],store:[1,3],str:1,strict:3,string:[3,4,6],submiss:1,submodul:8,subpackag:8,subscrib:[0,8],success:[4,5],successfulli:1,summari:1,support:4,sure:1,system:5,taken:1,templat:[0,5,8],test:[0,8],test_404_not_found:5,test_add_car:5,test_auth:[0,8],test_book:[0,8],test_booking_in_mybook:5,test_cancel_book:5,test_car:[0,8],test_car_manag:[0,8],test_change_car_detail:5,test_confirm_book:5,test_dashboard_rout:5,test_filter_after_book:5,test_filter_car:5,test_filter_invalid:5,test_fixtur:[0,8],test_login_invalid:5,test_login_unregist:5,test_login_valid:5,test_logout:5,test_register_invalid:5,test_register_valid:5,test_remove_car:5,test_render_index:5,test_render_login:5,test_render_regist:5,test_search:5,test_search_loc:5,test_search_mak:5,test_search_not_found:5,test_setup:5,test_unauthoris:5,test_view_all_car:5,test_view_book:5,test_view_first_car:5,than:5,thi:[3,4],time:[1,5],topic:4,totaldist:3,two:1,type:[0,1,3,4,6],unauthoris:[1,5],under:5,unit:5,unlock:[1,4],unregist:5,use:[1,4],used:[1,5],user:[0,1,4,5,8],user_data_set:4,userdata:4,userid:3,usermixin:3,usermodel:3,usernam:[1,3],username_valid:[0,8],usernamevalid:6,userschema:3,usertyp:3,valid:[0,1,5,8],valu:[2,5,6],verifi:1,verify_login:1,via:4,view:[1,5],walsh:0,well:0,when:[4,5],which:[1,5],white:0,william:0,yellow:0},titles:["MasterCSS package","MasterCSS.controllers package","MasterCSS.exceptions package","MasterCSS.models package","MasterCSS.mqtt package","MasterCSS.tests package","MasterCSS.validators package","Welcome to Carshare\u2019s documentation!","MasterCSS"],titleterms:{auth:1,book:[1,3],car:[1,3],carshar:7,cli:0,constant:0,content:[0,1,2,3,4,5,6],control:1,databas:0,document:7,email_valid:6,error_value_except:2,except:2,indic:7,mastercss:[0,1,2,3,4,5,6,8],model:3,modul:[0,1,2,3,4,5,6],mqtt:4,packag:[0,1,2,3,4,5,6],phone_valid:6,publish:4,submodul:[0,1,2,3,4,5,6],subpackag:0,subscrib:4,tabl:7,templat:1,test:5,test_auth:5,test_book:5,test_car:5,test_car_manag:5,test_fixtur:5,user:3,username_valid:6,valid:6,welcom:7}})