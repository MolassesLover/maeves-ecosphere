{
  description =
    "A tile-based procedural ecosystem simulation, with an object component system.";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];

      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in {
      packages = forAllSystems (system:
        let
          pkgs = (import nixpkgs { inherit system; });
          maeves-ecosphere = pkgs.callPackage misc/nix/package.nix { };
        in {
          inherit maeves-ecosphere;
          default = maeves-ecosphere;
          devShell = pkgs.mkShell { inputsFrom = [ maeves-ecosphere ]; };
        });
    };
}
