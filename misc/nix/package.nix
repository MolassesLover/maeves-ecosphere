{
  lib,
  python314Packages,
  callPackage,
}:
with python314Packages;
buildPythonApplication {
  pname = "maeves-ecosphere";
  version = "0.1.0";

  buildInputs = [
    cython
  ];

  propagatedBuildInputs = [
	  pygame
  ];

  pyproject = true;
  build-system = [ setuptools ];

  src = ../../.;
}
