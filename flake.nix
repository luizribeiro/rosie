{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
      dependencies = pkgs: with pkgs; [
        git
        (ollama.override {
          llama-cpp = (llama-cpp.override {
            cudaSupport = true;
            openblasSupport = false;
          });
        })
        (python310.withPackages (p: [
          p.aiohttp
          p.aiomqtt
          p.beautifulsoup4
          p.fastapi
          p.langchain
          p.openai
          p.pytz
          p.rich
          p.typer
          p.uvicorn
        ]))
      ];
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
      });

      devShells = forEachSystem
        (system:
          let
            pkgs = import nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  dotenv.enable = true;
                  packages = dependencies pkgs;
                }
              ];
            };
          });
    };
}
