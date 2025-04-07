using SDR.Core.API.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace SDR.Core.API.Services
{
    public interface IStudyDefinitionService
    {
        Task<IEnumerable<StudyDefinition>> GetAllAsync();
        Task<StudyDefinition> GetByIdAsync(string id);
        Task<StudyDefinition> CreateAsync(StudyDefinition studyDefinition);
        Task UpdateAsync(StudyDefinition studyDefinition);
        Task DeleteAsync(string id);
    }
}
