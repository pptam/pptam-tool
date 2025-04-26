helm install originx originx/originx \
              --set global.skywalkingaddress="ts-skywalking-helm-oap.ts.svc.cluster.local" \
              --set global.portalp2p.username="lincyaw" \
              --set global.portalp2p.password="SZj6c2cUVTzqaAX" \
              -n originx --create-namespace