{
  description = "lead scoring deployment";
  inputs = {
    root.url = "path:..";
    nixpkgs.follows = "root/nixpkgs";
  };
  outputs = { self, root, nixpkgs }:
  let system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      # reuse the root's common packages and add deployment needs.
      pythonEnv = root.lib.${system}.mkPythonEnv {
        extraPackages = ps: with ps; [
          uvicorn fastapi
        ];
      };
      image = pkgs.dockerTools.buildLayeredImage {
        name = "lead-score";
        tag = "latest";
        contents = [ pythonEnv ];
        extraCommands = ''
          mkdir -p app
          cp ${./predict.py} app/predict.py
          cp ${./pipeline.bin} app/pipeline.bin
        '';

        config = {
          WorkingDir = "/app";
          Cmd = [
            "${pythonEnv}/bin/uvicorn"
            "predict:app"
            "--host" "0.0.0.0"
            "--port" "9696"
          ];
          ExposedPorts = {
            "9696/tcp" = {};
          };
        };
      };
  in {
    packages.${system}.lead-score-image = image;
    devShells.${system}.default = pkgs.mkShell {
      packages = [ pythonEnv ];
    };
  };
}
