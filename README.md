# HWAPI
Hello World API App return users birthday message implemented with flaks and postgres on k8s

Docker images for the postgres DB and flask application have been created and commited to dockerhub.
I have used the same images from dockerhub in the k8s manifests.


You may run the initk8s.sh script to provision the app:
 - which creates secrets
 - deploys postgres app with emptydir persistent volume
 - deploys the helloworld app for api calls
 
 Get the Users Information:
 
 curl http://$(kubectl get svc | grep helloworld |awk '{print $4}')/user
