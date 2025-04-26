from diagrams import Cluster, Diagram
from diagrams.digitalocean.database import DbaasPrimaryStandbyMore
from diagrams.digitalocean.network import Domain
from diagrams.generic.network import Firewall, Router
from diagrams.generic.os import Raspbian
from diagrams.onprem.analytics import PowerBI
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import FastAPI
from diagrams.saas.cdn import Cloudflare

with Diagram(
    "Youtube API Webapp",
    show=False,
    filename="home_server",
    direction="LR",
):
    # Users
    users = Users("Users")

    # WAN
    with Cluster("Wide Area Network"):
        world_wide_web = Domain(label="somewebsite.com")
        youtube_api = DbaasPrimaryStandbyMore(label="Youtube APIs")

    # DNS
    with Cluster("Content Delivery Networks (CDN) Providers"):
        cloudflare_firewall = Firewall("CloudFlare Firewall")
        cloudflare = Cloudflare("CloudFlare Server")

    # LAN
    with Cluster("Local Area Network"):
        local_firewall = Firewall("Local Server Firewall")
        wifi_router = Router("192.1.****")

        # Home Server
        with Cluster("Home Server"):
            server = Raspbian("Rapsberry Pi\n(192.1.******)")
            nginx = Nginx("Nginx Load Balancer")

            # Containers
            with Cluster("Portainer"):
                webapp_1 = Docker("Containerized App 1\n(192.1.***1)")
                webapp_2 = Docker("Containerized App 2\n(192.1.***2)")
                webapp_3 = Docker("Containerized App 3\n(192.1.***3)")
                webapps = [webapp_1, webapp_2, webapp_3]

            # Containerized App
            with Cluster("Containerized App 1 \n (192.1.***1)"):
                airflow = Airflow("Staging (ETL Python)")
                postgres_db = PostgreSQL("Database")

                with Cluster("Consumption Zone"):
                    backend_data_apis = FastAPI("Backend\nData APIs")
                    backend_ml_model_apis = FastAPI("Backend\nML Model APIs")
                    dashboard = PowerBI(
                        "Dashboard \n (Power BI, plotly-dash, etc.)"
                    )

    # Diagram flow
    # From WWW
    users >> world_wide_web >> cloudflare_firewall >> cloudflare
    cloudflare >> local_firewall >> wifi_router >> nginx
    nginx >> webapps

    # Webapp 1
    webapp_1 >> airflow
    youtube_api >> airflow >> postgres_db
    postgres_db >> backend_data_apis
    backend_data_apis >> dashboard
    backend_ml_model_apis >> dashboard
