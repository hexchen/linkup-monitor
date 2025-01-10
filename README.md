
# Usage:
1. copy linkup_config.yaml.skel to linkup_config.yml and fill it with values (email and password are mandatory, unless you already have a token and account-id
```
auth:
  token: ey.....
  account-id: 
  email: paula@pinkepank.com
  password: <top-secret>
measurement:
  unit: 0  # 0: mmol/L; 1: mg/dL
```
2. run the container using the pre-built image
```
podman run -d --restart=always -p 8000:8000 --name linkup -v $(pwd)/linkup_config.yaml:/app/linkup_config.yaml:z martinstiehr/linkup-monitor:latest
```
the `-p 8000:8000` is only required, if you are interested in collecting the glucose measurements as metrics: `curl localhost:8000/metrics` 

3. alternatively build your own image:
```
buildah build -f Dockerfile -t linkup-monitor:0.1 .
