{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      p2n = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      rosie = p2n.mkPoetryApplication {
        projectDir = ./.;
        preferWheels = true;
      };
    in
    {
      packages.${system} = {
        inherit rosie;
        default = rosie;
      };

      apps.${system}.default = {
        type = "app";
        program = "${rosie}/bin/rosie";
      };

      devShells.${system}.default = pkgs.mkShell {
        inputsFrom = [ self.packages.${system}.rosie ];
      };
    };
}
