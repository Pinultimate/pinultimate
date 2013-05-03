
var ClusteringProcessor = function(data) {
	var K = 2;
	var clusters = [];

	var ClusterCenter = function(latitude, longitude) {
		this.latitude = latitude;
		this.longitude = longitude;
		this.center = {"latitude": this.latitude, "longitude": this.longitude};
		this.locations = [];
	}

	ClusterCenter.prototype.getCluster = function() {
		var count = 0;
		var length = this.locations.length;
		for (var i = 0; i < length; i++) {
			count += this.locations[i]['count'];
		}
		return {"latitude": this.latitude, "longitude": this.longitude, "count": count};
	}

	ClusterCenter.prototype.clearLocation = function() {
		this.locations = [];
	}

	ClusterCenter.prototype.addLocation = function(location) {
		this.locations.push(location);
	}

	ClusterCenter.prototype.getLocations = function() {
		return this.locations;
	}

	ClusterCenter.prototype.distance = function(location) {
		return dist(this.center, location);
	}
 
	ClusterCenter.prototype.getInfo = function() {
		console.log("latitude " + this.latitude + " longitude " + this.longitude + " locations " + this.locations);
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
		return (point1['latitude'] == point2['latitude']) && (point1['longitude'] == point2['longitude']);
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

	var updateCenters = function(centers) {
		var reassignment = 0;
		for (var i = 0; i < K; i++) {
			var newCenter = findCenter(centers[i].getLocations());
			if (!equals(newCenter, centers[i])) {
				centers[i] = newCenter;
				reassignment++;
			}
		}
		return reassignment;
	}	

	var initClusters = function() {
		var a = findCenter(data['0']);
		var b = findCenter(data['1']);
		var centers = [a, b];
		a.getInfo();
		b.getInfo();
		
		return centers;
	}

	var putLocationsInCenters = function(centers, locations) {
		for (var j = 0; j < K; j++) {
			centers[j].clearLocation();
		}
		var n = locations.length;
		for (var i = 0; i < n; i++) {
			findCluster(locations[i], centers).addLocation(locations[i]);
		}
	}

	var runKMeans = function(centers, locations) {
		while (true) {
			putLocationsInCenters(centers, locations);
			var reassignment = updateCenters(centers);
			if (reassignment == 0) break;
		}
		return centers;
	}

	var createClusters = function(centers) {
		for (var i = 0; i < K; i++) {
			clusters[i] = centers[i].getCluster();
		}
	}

	var cluster = function() {
		var centers = initClusters(data);
		centers = runKMeans(centers, data['0']);
		createClusters(centers);
	}

	var test = function() {
		var centers = initClusters(data);
		var count = 0;
		while (true) {
			count++;
			putLocationsInCenters(centers, data['0']);
			var reassignment = updateCenters(centers);
			if (reassignment == 0) break;
			if (count == 100) break;
			centers[0].getInfo();
			centers[1].getInfo();
		}



	}

	//test();
	cluster();
	return clusters;

}

