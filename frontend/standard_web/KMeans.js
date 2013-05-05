
var ClusteringProcessor = function(data) {
	var K = 2;
	var clusters = [];

	var ClusterCenter = function(latitude, longitude) {
		this.latitude = latitude;
		this.longitude = longitude;
		this.count = 1;
		this.center = {"latitude": this.latitude, "longitude": this.longitude, "count": 1};
		this.locations = [this.center];
	}

	ClusterCenter.prototype.getCluster = function() {
		var count = 0;
		var length = this.locations.length;
		var radius = 0;
		for (var i = 0; i < length; i++) {
			count += this.locations[i]['count'];
			if (this.locations[i]['distance'] > radius) {
				radius = this.locations[i]['distance'];
			}
		}
		return {"latitude": this.latitude, "longitude": this.longitude, "count": count, "radius": Math.sqrt(radius)};
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
			var newCenter;
			if (centers[i].getLocations().length == 0) {
				newCenter = centers[i];
			} else {
				newCenter = findCenter(centers[i].getLocations());
			}
			if (!equals(newCenter, centers[i])) {
				centers[i] = newCenter;
				reassignment++;
			}
		}
		return reassignment;
	}	

	var calculateCost = function(locations, centers) {
		var sum = 0;
		var length = locations.length;
		for (var i = 0; i < length; i++) {
			var distance = findCluster(locations[i], centers).distance(locations[i]);
			locations[i]['distance'] = distance;
			sum += distance;
		}
		return sum;
	}

	var KMeansLine = function(locations) {

		var NUM_IT = 5;
		var l = K * 2;
		var centers = [];
		var index = Math.floor(Math.random()*locations.length);
		var initLoc = locations[index];
		locations.splice(index, 1);
		centers.push(new ClusterCenter(initLoc['latitude'], initLoc['longitude']));

		var sum = calculateCost(locations, centers);

		var length = locations.length;

		for (var i = 0; i < NUM_IT; i++) {
			for (var j = 0; j < length; j++) {
				var prob = l * Math.random() * sum;
				if (prob - locations[j]['distance'] > 0) continue;
				centers.push(new ClusterCenter(locations[j]['latitude'], locations[j]['longitude']));
				locations.splice(j, 1);
				length--;
				j--;
			}
			sum = calculateCost(locations, centers);
			if ((i == NUM_IT - 1) && (centers.length < K)) NUM_IT += NUM_IT;
		}
		return centers;
	}

	var KMeansPlus = function(locations) {
		var centers = [];
		var index = Math.floor(Math.random()*locations.length);
		var initLoc = locations[index];
		locations.splice(index, 1);
		centers.push(new ClusterCenter(initLoc['latitude'], initLoc['longitude']));

		var sum = calculateCost(locations, centers);

		var length = locations.length;
		var FLAG = false;
		while (true) {
			for (var j = 0; j < length; j++) {
				var prob = locations[j]['weight'] * Math.random() * sum;
				if (prob - locations[j]['distance'] > 0) continue;
				centers.push(new ClusterCenter(locations[j]['latitude'], locations[j]['longitude']));
				locations.splice(j, 1);
				length--;
				j--;
				if (centers.length == K) {
					FLAG = true;
					break;
				}
			}
			if (FLAG == true) break;
			sum = calculateCost(locations, centers);
		}
		return centers;
		
	}

	var recluster = function(oldCenters) {
		var n = oldCenters.length;
		for (var j = 0; j < n; j++) {
			oldCenters[j]['weight'] = 0;
		}
		var length = data.length;
		for (var i = 0; i < length; i++) {
			findCluster(data[i], oldCenters)['weight']++;
		}
		var centers = KMeansPlus(oldCenters.slice(0));

		return runKMeans(centers, oldCenters);
	}

	var initClusters = function() {
		var centers = KMeansLine(data.slice(0));
		return recluster(centers);
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
		var count = 0;
		while (true) {
			count++;
			putLocationsInCenters(centers, locations);
			var reassignment = updateCenters(centers);

			if (reassignment == 0 || count > 2000) {
				break;
			}
		}
		putLocationsInCenters(centers, locations);
		return centers;
	}

	var createClusters = function(centers) {
		for (var i = 0; i < K; i++) {
			clusters[i] = centers[i].getCluster();
		}
	}

	var cluster = function() {
		var centers = initClusters();
		centers = runKMeans(centers, data);
		createClusters(centers);
	}

	var test = function() {
		
	}

	//test();
	cluster();
	console.log(clusters);
	return clusters;

}

