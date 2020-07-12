# @Author: Dongqing Sun
# @Date:   2020-07-12 18:37:18
# @Last Modified by:   Dongqing Sun
# @Last Modified time: 2020-07-12 18:37:24


# From tongji to aws
rsync -ravP -e 'ssh -i login_seoul.pem' /home1/wangchenfei/Project/SingleCell/WebServer/TISCH/static/data ubuntu@ec2-54-180-163-127.ap-northeast-2.compute.amazonaws.com:/home/ubuntu/projects/TISCH/static/ 

# Form aws to tongji
rsync -ravP -e 'ssh -i login_seoul.pem' ubuntu@ec2-54-180-163-127.ap-northeast-2.compute.amazonaws.com:/home/ubuntu/projects/TISCH/static/data /home1/wangchenfei/Project/SingleCell/WebServer/TISCH/static/

# From tongji to ali
rsync -ravP -e 'ssh ' /home1/wangchenfei/Project/SingleCell/WebServer/TISCH/static/data dongqing@39.101.160.221:/data/dongqing/TISCH/static/