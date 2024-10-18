resource "aws_security_group" "proxy_security_group" {
  name        = "proxy_security_group"
  description = "Security group for the Quantum Safe TLS Proxy"
  vpc_id      = "vpc-xxxxxxxx"

  # Allow inbound TLS traffic
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "proxy-security-group"
  }
}
