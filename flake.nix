{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { nixpkgs, poetry2nix, ... }:
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
        # replace <script> with the name in the [tool.poetry.scripts] section of your pyproject.toml
        program = "${rosie}/bin/rosie";
      };
    };
}
