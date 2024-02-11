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
      overlays = [
        (self: super: {
          python310 = super.python310.override {
            packageOverrides = self: super: {
              langchain = super.langchain.overridePythonAttrs (old: {
                disabledTests = old.disabledTests ++ [
                  "test_create_sql_agent"
                  "test_convert_pydantic_to_openai_function"
                  "test_convert_pydantic_to_openai_function_nested"
                ];
              });
            };
          };
        })
      ];
      dependencies = pkgs: with pkgs; [
        (ollama.override {
          llama-cpp = (llama-cpp.override {
            cudaSupport = true;
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
      devDependencies = pkgs: with pkgs; [
        nodePackages.pyright
      ];
    in
    {
      packages = forEachSystem
        (system:
          let
            pkgs = import nixpkgs {
              inherit system overlays;
              config.allowUnfree = true;
            };
          in
          {
            devenv-up = self.devShells.${system}.default.config.procfileScript;
            rosie = pkgs.stdenv.mkDerivation {
              name = "rosie";
              src = ./.;
              nativeBuildInputs = [ pkgs.makeWrapper ];
              buildInputs = dependencies pkgs;
              buildPhase = ''
                mkdir -p $out/{bin,share/rosie}
                cp -r src $out/share/rosie/src
                cp rosie $out/share/rosie/rosie
                wrapProgram $out/share/rosie/rosie \
                  --prefix PYTHONPATH : $out/share/rosie/src
                ln -s $out/share/rosie/rosie $out/bin/rosie
              '';
            };
          });

      devShells = forEachSystem
        (system:
          let
            pkgs = import nixpkgs {
              inherit system overlays;
              config.allowUnfree = true;
            };
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  dotenv.enable = true;
                  packages = (dependencies pkgs)
                    ++ (devDependencies pkgs);
                }
              ];
            };
          });
    };
}
