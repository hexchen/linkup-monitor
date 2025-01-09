# Usage:
1. copy linkup_config.yaml.skel to linkup_config.yml and fill it with values (email and password are mandatory, unless you already have a token and account-id
```
auth:
  token: ey.....
  account-id: 
  email: paula@pinkepank.com
  password: <top-secret>
```
2. build the container image (optional) 
```
buildah build -f Dockerfile -t linkup-client:0.0.1 .
```
3. run the container 
```
podman run -d --restart=always -p 8000:8000 -v $(pwd)/linkup_config.yaml:/app/linkup_config.yaml:z linkup-client:1
```
the `-p 8000:8000` is only required, if you are interested in collecting the glucose measurements as metrics: 
`curl localhost:8000/metrics` 

# todo
* fix logging in container
