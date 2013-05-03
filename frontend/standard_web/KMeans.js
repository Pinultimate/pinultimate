
var ClusteringProcessor = function(data) {
	var K = 10;
	var clusters = [];






	var ClusterCenter = function(latitude, longitude) {
		this.latitude = latitude;
		this.longitude = longitude;
		this.center = {"latitude": this.latitude, "longitude": this.longitude};
	}

	ClusterCenter.prototype.distance = function(location) {
		return dist(this.center, location);
	}
 
	ClusterCenter.prototype.getInfo = function() {
		console.log("latitude " + this.latitude + " longitude " + this.longitude)
	}

	ClusterCenter.prototype.radius = function(locations) {
		var result = 0;
		var center = this.center;
		var length = locations.length;

		for (var i = 0; i < length; i++) {
			var distance = dist(center, locations[i]);
			if (distance > result) {
				result = distance;
			}
		}
		return result;
	}

	var findCenter = function(locations) {
		var count = 0;
		var lat = 0;
		var lon = 0;
		var length = locations.length;
		for (var i = 0; i < length; i++) {
			count += locations[i]['count'];
			lat += locations[i]['latitude'] * locations[i]['count'];
			lon += locations[i]['longitude'] * locations[i]['count'];
		}
		lat = lat / count;
		lon = lon / count;		
		return new ClusterCenter(lat, lon);
	}

	var dist = function(point1, point2) {
		return Math.pow(point1['latitude'] - point2['latitude'], 2) + Math.pow(point1['longitude'] - point2['longitude'], 2);
	}

	var equals = function(point1, point2) {
		return (point1['latitude'] == point2['latitude']) && (point1['longitude'] - point2['longitude']);
	}

	var findCluster = function(location, centers) {
		var result = centers[0];
		var minDist = centers[0].distance(location);

		var length = centers.length;
		for (var i = 1; i < length; i++) {
			var distance = centers[i].distance(location);
			if (distance < minDist) {
				minDist = distance;
				result = centers[i];
			}
		}
		return result;
	}


	var initClusters = function() {
		var a = findCenter(data['0']);
		var b = findCenter(data['1']);
		var centers = [a, b];
		a.getInfo();
		b.getInfo();
		var c = findCluster(data['0'][1], centers);
		c.getInfo();
	}


	initClusters();
	return clusters;

}

