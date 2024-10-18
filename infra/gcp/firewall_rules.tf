resource "google_compute_firewall" "proxy_firewall" {
  name    = "proxy-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["proxy-service"]
}
