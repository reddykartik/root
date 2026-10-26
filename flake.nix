{
  description = "environment setup";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/02f754064dce1a8c2b4b301f25c43b44fe2bbfd";
  outputs = { self, nixpkgs }:
  let system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      # shared python dependencies plus optional project-specific ones.
      mkPythonEnv = { extraPackages ? (_: []) }:
        pkgs.python314.withPackages (ps: 
          (with ps; [
            numpy pandas scikit-learn
          ]) ++ extraPackages ps
        );
  in {
    # shared function that child project flakes can reuse.
    lib.${system}.mkPythonEnv = mkPythonEnv;
    
    # keep the root development environment.
    devShells.${system}.default = pkgs.mkShell {
      packages = [ (mkPythonEnv {
        extraPackages = ps: with ps; [
          matplotlib seaborn notebook
        ];
      })];
    };
  };
}
