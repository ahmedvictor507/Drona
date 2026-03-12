# Information: https://drona.coex.tech/en/simple_offboard.html#gettelemetry

import rospy
from drona import srv

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)

# Print drone's state
print(get_telemetry())
