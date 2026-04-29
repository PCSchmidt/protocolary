using Microsoft.AspNetCore.Mvc;
using SDR.Core.API.Models;
using SDR.Core.API.Services;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace SDR.Core.API.Controllers
{
    [ApiController]
    [Route("api/v3/[controller]")]
    public class StudyDefinitionsController : ControllerBase
    {
        private readonly IStudyDefinitionService _studyDefinitionService;

        public StudyDefinitionsController(IStudyDefinitionService studyDefinitionService)
        {
            _studyDefinitionService = studyDefinitionService;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<StudyDefinition>>> GetAll()
        {
            try
            {
                var studyDefinitions = await _studyDefinitionService.GetAllAsync();
                return Ok(studyDefinitions);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<StudyDefinition>> Get(string id)
        {
            try
            {
                var studyDefinition = await _studyDefinitionService.GetByIdAsync(id);
                if (studyDefinition == null)
                {
                    return NotFound($"Study definition with ID {id} not found");
                }
                return Ok(studyDefinition);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpPost]
        public async Task<ActionResult<StudyDefinition>> Create([FromBody] StudyDefinition studyDefinition)
        {
            try
            {
                if (studyDefinition == null)
                {
                    return BadRequest("Study definition cannot be null");
                }

                var createdStudyDefinition = await _studyDefinitionService.CreateAsync(studyDefinition);
                return CreatedAtAction(nameof(Get), new { id = createdStudyDefinition.Id }, createdStudyDefinition);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(string id, [FromBody] StudyDefinition studyDefinition)
        {
            try
            {
                if (studyDefinition == null)
                {
                    return BadRequest("Study definition cannot be null");
                }

                if (id != studyDefinition.Id)
                {
                    return BadRequest("ID in URL does not match ID in study definition");
                }

                var existingStudyDefinition = await _studyDefinitionService.GetByIdAsync(id);
                if (existingStudyDefinition == null)
                {
                    return NotFound($"Study definition with ID {id} not found");
                }

                await _studyDefinitionService.UpdateAsync(studyDefinition);
                return NoContent();
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(string id)
        {
            try
            {
                var existingStudyDefinition = await _studyDefinitionService.GetByIdAsync(id);
                if (existingStudyDefinition == null)
                {
                    return NotFound($"Study definition with ID {id} not found");
                }

                await _studyDefinitionService.DeleteAsync(id);
                return NoContent();
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}
