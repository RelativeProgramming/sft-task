# sft-task

## My Results

### MariaDB
Average Insertions per second: 410.4

All measurements:
401 409 406 405 398 414 413 426 409 423

### MariaDB-Galera
TODO

## How To Use

Start Minikube with 3 nodes:
```
minikube start --nodes 3
```

Run local Docker Registry with Minikube:
```
docker run --rm -it --network=host alpine ash -c "apk add socat && socat TCP-LISTEN:5000,reuseaddr,fork TCP:$(minikube ip):5000"
```

Build/Push writer script (inside project directory):
```
docker build -t localhost:5000/sft-writer .
```
```
docker push localhost:5000/sft-writer
```

Deploy MariaDB/MariaDB-Galera onto cluster:
```
helm install my-release bitnami/mariadb --set volumePermissions.enabled=true --set auth.rootPassword=test --set auth.database=test
```
or
```
helm install my-release bitnami/mariadb-galera --set rootUser.password=test --set db.name=test -f mariadb-galera-init-config.yaml 
```

Deploy writer script:
```
kubectl apply -f deployment-mariadb.yml
```
or
```
kubectl apply -f deployment-mariadb-galera.yml
```

After ~10s view logs of writer pod for result:
```
kubectl logs POD_NAME
```

# Utilities
Show all running pods:
```
kubectl get pod
```

Delete writer deployment:
```
kubectl delete deployment writer
```