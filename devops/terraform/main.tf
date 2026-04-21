provider "local" {
}

resource "local_file" "example" {
  filename = "demo.txt"
  content  = "Hello DevOps - Terraform Working"
}