# scoutshop_groups.webservice

<H3>Consulta</H3>

https://mirlo.guiasyscouts.cl:8080/validador?group=<id_grupo>[&year=<año>]

<H3>pre-requisites</H3>
you must install:

sudo dnf install postgresql<br/>
sudo dnf install bcrypt<br/>
sudo dnf install openssl<br/>
sudo dnf install python3-devel<br/>
sudo dnf -y groupinstall "Development Tools"<br/>
pip install flask<br/>
pip install flask_restful<br/>
pip install bcrypt<br/>
pip install psycopg2<br/>


<H3>Develop</H3>
In dev environment you must use the db.ini within the folder webservice


<H3>Production</H3>
In prod environment you have to config the database info in the db.ini file at the root folder<br/>
In prod this run with apache2 + python3 + wsig
